use v5.42;
my $r = eval { 1 / 0 }; print defined $r ? "d" : "u:", ($@ =~ /division/ ? "div" : "?"), "\n";
