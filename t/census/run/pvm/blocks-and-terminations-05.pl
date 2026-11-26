use v5.42;
my $t = time;
print $t > 1000000000 ? "past" : "impossible", "\n";
