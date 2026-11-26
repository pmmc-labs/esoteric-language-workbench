use v5.42;
my @d=(4,0,2); my $s=0; for (@d) { next unless $_; $s+=8/$_ } print "$s\n";
