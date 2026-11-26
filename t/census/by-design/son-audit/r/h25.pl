use v5.42;
our @g=(1,2,3); sub sw { @g[0,2]=@g[2,0] } sw(); print "@g\n";
