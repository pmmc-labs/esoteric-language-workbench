# kind: refused
# perl: the line of the block's statement, 2; refused, the block being one statement over two lines.
use v5.42;
my @a = map { $_ == 2 ?
  die("m") : $_ } (1, 2);
