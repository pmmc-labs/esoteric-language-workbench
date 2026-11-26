use v5.42;
our $g = 1; my $c = sub { local $g = 2; $g }; my $v = $c->(); print "$g $v\n";
