use v5.42;
my $s=""; for my $w (qw(a b)) { for ($w) { $s.=$_; } $s.=$w } print "$s\n";
