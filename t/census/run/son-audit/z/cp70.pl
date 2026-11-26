use v5.42;
my $h={l=>[1,2]}; my @c=@{$h->{l}}; @{$h->{l}}=(9); print "@c\n";
