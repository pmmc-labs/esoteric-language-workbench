use v5.42;
my %h=(a=>1,b=>2); my %i=reverse %h; print join(",",map{"$_$i{$_}"}sort keys %i),"\n";
