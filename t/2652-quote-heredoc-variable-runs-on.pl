# kind: refused
# perl reads the index across the line as code: 1.
use v5.42;
my @a = (1);
print <<"EOT";
$a[
0]
EOT
