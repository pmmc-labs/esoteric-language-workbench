# kind: fault
# model: t/models/bool.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
say(1);
say(('[' . substr(false, 0)) . ']');
say(substr((undef), 0));
say(2);
