use v5.42;
my $lo = -9223372036854775807 - 1 + 513;
for my $i ($lo .. $lo + 1) { say $i; }
say "ok";
$lo = $lo - 1;
for my $i ($lo .. $lo + 1) { say $i; }
say "not reached";
