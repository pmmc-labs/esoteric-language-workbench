use v5.42;
BEGIN { our $early = "b" } our $early; my $late = "l"; print "$early$late\n";
