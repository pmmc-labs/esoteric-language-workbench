# kind: refused
# perl would take it, if $x were set as it compiles.
use v5.42;
my $x = ':std';
use open "$x", ':encoding(UTF-8)';
