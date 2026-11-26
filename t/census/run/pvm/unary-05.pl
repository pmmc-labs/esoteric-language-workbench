use v5.42;
my %h;
my $a1 = $h{a}++;
my $a2 = $h{a}++;
my $b1 = ++$h{b};
my $b2 = ++$h{b};
print "$a1 $a2 $h{a} $b1 $b2 $h{b}\n";
