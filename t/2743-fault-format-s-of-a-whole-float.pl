# kind: fault
# perl prints 1e+15; the language prints no whole Num from 10^15 (D36).
use v5.42;
say sprintf("%s", 1e15);
