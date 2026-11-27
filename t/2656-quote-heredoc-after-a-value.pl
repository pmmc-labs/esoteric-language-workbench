# kind: refused
# perl takes $x for a file handle: Can't use string ("1") as a symbol ref. Here << after a value is the left shift, not in the language.
use v5.42;
my $x = 1;
say $x <<EOT;
EOT
