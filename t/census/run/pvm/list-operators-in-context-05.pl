use v5.42;
my @a = qw(x y z);
$a[0] = $ENV{G};
my @block = grep { $_ } @a;
my @expr  = grep($_, @a);
my $n = grep { $_ } @a;
print "@block @expr $n\n";
