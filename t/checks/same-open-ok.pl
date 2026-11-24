# check: ok
# With `use open`, perl prints UTF-8 (D39).
use v5.42;
use open ':std', ':encoding(UTF-8)';
say "\x{e9}\x{263A}";
