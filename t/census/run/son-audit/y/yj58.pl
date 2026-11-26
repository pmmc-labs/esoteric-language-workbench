use v5.42;
$_ = "keep"; my $n = () = "abc" =~ /./g; print "$_$n\n"; for my $w (qw(a)) { $_ .= "!" } print "$_\n";
