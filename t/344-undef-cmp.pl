# kind: fault
# model: t/models/bool.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
say("" cmp false);
say("" cmp (undef));
say(2);
