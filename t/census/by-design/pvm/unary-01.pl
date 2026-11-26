use v5.42;
my $a = $ENV{X} // 5;
my $b = $a++;
my $c = ++$a;
my $d = $a--;
my $e = --$a;
print "$a $b $c $d $e\n";
