# kind: fault
# model: t/models/bool.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
say(0 ? (undef) : 'else');
say(1 ? (undef) : 'else');
say(2);
