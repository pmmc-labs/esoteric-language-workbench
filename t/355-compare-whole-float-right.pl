# kind: fault
# model: t/models/bool.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
say('x' cmp 9007199254740992.0);
say('x' cmp 9007199254740991.0);
say(2);
