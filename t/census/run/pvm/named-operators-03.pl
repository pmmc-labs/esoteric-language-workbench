use v5.42;
my $n = $ENV{X} // 74;
my $live = chr($n);
my $folded = chr(74);
my $back = ord($live);
print "[$live][$folded][$back]\n";
