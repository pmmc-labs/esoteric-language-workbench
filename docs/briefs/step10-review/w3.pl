use v5.42;
# W3: `@a = sort BLOCK @a` is done in place, and perl's in-place sort drops every
# element that was never stored (pp_sort.c: "Weed out nulls"). Whether an undef
# element was "ever stored" is the array's past: map, grep, a call and a plain sort fill them in.
my @d = (3); $d[3] = 1;
@d = sort { ($a // 0) <=> ($b // 0) } @d;
say scalar(@d), ": ", join(",", map { $_ // "u" } @d);

my @e = (3, undef, undef, 1);                    # the same values, each stored
@e = sort { ($a // 0) <=> ($b // 0) } @e;
say scalar(@e), ": ", join(",", map { $_ // "u" } @e);

my @f = (3); $f[3] = 1;
my @copy = sort { ($a // 0) <=> ($b // 0) } @f;  # not in place: four
say scalar(@copy);

my @g = (3); $g[3] = 1;
@g = reverse sort { ($a // 0) <=> ($b // 0) } @g;   # not in place either: four
say scalar(@g);

my @h = (3); $h[3] = 1;
my @m = grep { 1 } @h;                           # grep makes the elements
@h = sort { ($a // 0) <=> ($b // 0) } @h;
say scalar(@h);

my @i = (3); $i[3] = 1;
for my $x (@i) { }                               # foreach does not
@i = sort { ($a // 0) <=> ($b // 0) } @i;
say scalar(@i);

my @j; $j[2] = 5;
@j = sort { 0 } @j;
say scalar(@j);
