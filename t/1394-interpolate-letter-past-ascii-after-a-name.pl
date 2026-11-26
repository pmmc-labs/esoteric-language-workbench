# kind: refused
# perl reads the name $x and an e-acute, which is not declared (T205).
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
my $x = "e";
say "$xé";
