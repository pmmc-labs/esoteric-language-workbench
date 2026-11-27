# kind: dies
# Past ASCII, with use open: UTF-8 on stderr (T307).
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
say "café";
die "☺ é";
