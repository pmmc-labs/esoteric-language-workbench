use v5.42;
$_ = "hello"; my $n = tr/l//; my $m = /ll/ ? "y" : "n"; s/h/J/; my @c = /(.)/g; print "$n$m$_", scalar(@c), "\n";
