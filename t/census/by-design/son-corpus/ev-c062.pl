use v5.42;
my $d = $ENV{X} // 0;
my $r = eval { 10 / $d } // "trapped";
print "$r\n";
