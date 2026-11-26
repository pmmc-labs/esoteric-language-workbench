use v5.42;
my $s="ab"; my @a=($s,$s); $a[0].="c"; print "$s @a\n";
