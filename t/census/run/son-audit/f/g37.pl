use v5.42;
my $o={l=>[1]}; my @c=@{$o->{l}}; push @{$o->{l}},2; print scalar(@c),"\n";
