use v5.42;
my @a = qw(x y z);
$a[0] = "$ENV{M}a";
my @block = map { $_ } @a;
my @expr  = map($_, @a);
my $n = map { $_ } @a;
print "@block @expr $n\n";
