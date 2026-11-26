use v5.42;
my %h; my $v = $h{x} //= 5; $h{x}++; print "$v$h{x}\n";
