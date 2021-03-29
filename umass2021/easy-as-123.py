import base64
import socket
import struct

data = b''
rows = []

with open('easy_as_123.pcap', 'rb') as f:
    header = f.read(24)
    while True:
        packet_header = f.read(16)
        if not packet_header:
            break
        ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', packet_header)
        raw_packet = f.read(incl_len)

        if (raw_packet[0x0E] & 0xF0) != 0x40: # IPv4?
            continue
        if raw_packet[0x17] != 0x06: # TCP?
            continue
        src_ip = socket.inet_ntoa(raw_packet[0x1A:0x1E])
        dest_ip = socket.inet_ntoa(raw_packet[0x1E:0x22])
        src_port, dest_port = struct.unpack('>HH', raw_packet[0x22:0x26])

        if src_ip != '192.168.1.19': # and dest_ip != '192.168.1.19':
            continue

        if not raw_packet[0x2F] & 0x08: # PSH?
            continue

        row = raw_packet[0x36:]
        rows.append(row)
        data += row
        #print('%d.%06d: %s:%d -> %s:%d: %d bytes' % (ts_sec, ts_usec, src_ip, src_port, dest_ip, dest_port, len(raw_packet)-0x36))

# 66 packets
#
# 139 bytes:
#    4 bytes fixed: SM\x92-
#    1 byte counter: 0xfe/0xff/0x00/0x01/0x02/0x03/0x04
#    6 bytes command: --help, --init, getflg, getjnk
#  128 bytes payload

# replace \x01 => \\1 (and ignore final \x00) in initial help text for some reason
# --help: "'init' command will alter implant to initialize data exfiltration. cmd 'get[a-z][a-z][a-z]' to exfil. "
# --init: "exfiltration initialized. switching protection. subsequent payload blocks protected in ctr mode.      "

# Counter values seen:
# help: 0 (fe), 17 (00), 62 (00) - 00's identical
# init: 1 (ff)
# getflg: 2 (00), 27 (00), 44 (02), 63 (01) - 00's identical
# getjnk: rest (00-04)

print(repr(base64.a85decode(rows[0][11:-1].replace(b'\x01', b'\\1'))))
print(repr(base64.a85decode(rows[1][11:])))

keystream = [a ^ b for a, b in zip(b"'init' command will alter implant to initialize data exfiltration. cmd 'get[a-z][a-z][a-z]' to exfil. ", rows[17][11:])]
for i, row in enumerate(rows):
    if row[4] == 0:
        dec = bytes(a ^ b for a, b in zip(row[11:], keystream))
        line = '%d:' % i
        for k in range(len(dec)):
            if dec[k] < 0x20:
                line += ' %d' % k
        print('%d: %r' % (i, dec))
