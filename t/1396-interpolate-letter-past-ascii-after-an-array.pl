# kind: refused
# perl reads the name @a and an e-acute, which is not declared.
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
my @a = (1, 2, 3);
say "@aé";
