use v5.42;
our @g=(1); sub n { push @g,2; 0 } my @l = (@g, n(), @g); print scalar(@l),"\n";
