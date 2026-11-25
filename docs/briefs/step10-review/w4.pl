use v5.42;
# W4: sort with a block makes an element or a slice past the end, as map, grep and
# foreach do. Only the four blocks perl optimises away ({ $a <=> $b } and its kin),
# and sort with no block, make nothing: T177-sort tried only `{ $a <=> $b }`.
my @r;
{ my @a = (1); @r = sort { ($a // 0) <=> ($b // 0) } @a[0 .. 3]; say "slice, a block:      ", scalar(@a); }
{ my @a = (1); @r = sort { ($a // 0) <=> ($b // 0) } $a[5], 1;   say "element, a block:    ", scalar(@a); }
{ my @a = (1); @r = sort { 0 } $a[5];                            say "one element:         ", scalar(@a); }
{ my @a = (1); @r = sort { 0 } (1 ? $a[5] : 0), 2;               say "through ? ::         ", scalar(@a); }
{ my @a = (1); @r = reverse sort { 0 } $a[5], 1;                 say "reverse sort:        ", scalar(@a); }
{ my @a = (1); for my $x (sort { 0 } $a[5], 1) { }               say "in a foreach:        ", scalar(@a); }
{ no warnings; my @a = (1); @r = sort { $a <=> $b } $a[5], 1;    say "{ \$a <=> \$b }:       ", scalar(@a); }
{ no warnings; my @a = (1); @r = sort $a[5], 1;                  say "no block:            ", scalar(@a); }
{ my @a = (1); @r = reverse($a[5], 1); my $j = join(",", $a[5] // 0); say "reverse, join:       ", scalar(@a); }
