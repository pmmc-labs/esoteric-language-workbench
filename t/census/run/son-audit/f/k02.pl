use v5.42;
sub mk { my $n=0; return (sub { $n++ }, sub { $n }) } my ($i,$g)=mk(); $i->(); $i->(); print $g->(),"\n";
