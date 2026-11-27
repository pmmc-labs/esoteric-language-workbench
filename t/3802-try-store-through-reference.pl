# kind: same
# Stores through references in a try stand after its die, as perl's do (T309, D107).
use v5.42;
my %h;
my $r = \%h;
try { $r->{x}{y} = 3; $h{z} = [4]; die "stop\n"; } catch ($e) { print $e; say $h{x}{y}, $r->{z}[0]; }
my @rows = ([1, 2], [3, 4]);
for my $row (@rows) { try { die "odd\n" if $row->[0] == 3; say $row->[1]; } catch ($e) { print "caught ", $e; } }
sub f($t) { try { $t->{n}++; return $t->{n}; } catch ($e) { return -1; } }
my $t = {};
say f($t), f($t);
