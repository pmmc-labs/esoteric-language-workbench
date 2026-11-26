use v5.42;
my $t = "x"; $t =~ /(?<n>x)/; my %c = %+; "y" =~ /(y)/; my @c = ($1, $&); "zz" =~ /z/; print "$c{n}@c$&$`|$'|", "\n";
