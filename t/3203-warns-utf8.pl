# kind: warns
# Past ASCII, with use open: UTF-8 on stderr (T307).
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
warn "café\n";
say STDERR "☺";
warn "é";
say "done";
