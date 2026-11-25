# kind: fault
# model: t/models/bool.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
say(('[' . (false x 2)) . ']');
say(('[' . ((undef) x 2)) . ']');
say(2);
