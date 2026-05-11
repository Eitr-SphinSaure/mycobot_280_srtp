# XSB 部分

*simple_test_en.xsb*
```prolog
% 1. 事实（原子：xiaoming、xiaohong、xiaoli 均小写开头）
student(xiaoming, math, 85).
student(xiaohong, math, 58).
student(xiaoming, english, 92).
student(xiaohong, english, 63).
student(xiaoli, math, 72).

% 2. 规则（变量：Student、Course、Score 均大写开头）
pass(Student, Course) :-
    student(Student, Course, Score),
    Score >= 60.

get_credit(Student, Course) :-
    pass(Student, Course).
```

*~/XSB/bin*
```bash
./xsb
['simple_test_en.xsb'].
spy(get_credit/2).
get_credit(xiaohong, Course).
notrace.
halt.
```

```bash
./xsb
['joint.xsb'].
spy(get_credit/2).
get_credit(xiaohong, Course).
notrace.
halt.
```

*output*
```bash
what@ubuntu:~/XSB/bin$ ./xsb
[xsb_configuration loaded]
[sysinitrc loaded]
[xsbbrat loaded]

XSB Version 5.0.0 (Green Tea) of May 15, 2022
[x86_64-pc-linux-gnu 64 bits; mode: optimal; engine: slg-wam; scheduling: local]
[Build date: 2025-11-28]

| ?- ['simple_test_en.xsb'].
[./simple_test_en.xsb loaded]

yes
| ?- spy(get_credit/2).
Spy point set on usermod:get_credit/2

yes
[debug]
| ?- get_credit(xiaohong, Course).
** (0) Call: get_credit(xiaohong,_h340) ? 
   (1) Call: pass(xiaohong,_h340) ? 
   (2) Call: student(xiaohong,_h340,_h457) ? 
   (2) Exit: student(xiaohong,math,58) ? 
   (2) Redo: student(xiaohong,math,58) ? 
   (2) Exit: student(xiaohong,english,63) ? 
   (1) Exit: pass(xiaohong,english) ? 
** (0) Exit: get_credit(xiaohong,english) ? 

Course = english

yes
[trace]
| ?- notrace.

yes
| ?- halt.

End XSB (cputime 0.03 secs, elapsetime 65.00 secs)
what@ubuntu:~/XSB/bin$ 
```