use v5.42;
my $x=1; my $inc=sub { $x++ }; my $get=sub { $x }; $inc->(); $inc->(); print $get->(), "\n";
