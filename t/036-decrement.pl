# kind: refused
# Two minus signs with nothing between them are one token, a decrement,
# and perl won't compile a decrement of 5 (T27). `say - -5;` is 5.
use v5.42;
say --5;
