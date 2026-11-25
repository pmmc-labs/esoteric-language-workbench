# kind: fault
# model: t/models/bool.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
say(100000000000000.0 eq false);
say(1000000000000000.0 eq (undef));
say(2);
