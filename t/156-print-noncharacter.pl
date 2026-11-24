# kind: fault
# model: t/models/str.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
say("\x{FFFD}");
say("\x{FFFE}");
say(2);
