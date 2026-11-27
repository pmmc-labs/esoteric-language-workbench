# A die through loops over an array and a hash, and a map, a grep and a sort,
# caught: each freeze is given back, each sort ended (D141, T308).
use v5.42;
my @a = (1, 2, 3);
my %h = (a => 1, b => 2);
sub over($n) {
    for my $x (@a) {
        for my $v (sort { $a <=> $b } values %h) {
            die "at $x $v\n" if $x == $n && $v == 2;
        }
    }
    return "none";
}
for my $n (1 .. 4) {
    try { say over($n) } catch ($e) { print $e; push @a, $n; $h{"k$n"} = $n }
}
say "@a";
say join(",", map { "$_=$h{$_}" } sort keys %h);
my @s = (5, 3, 8, 1);
for my $k (1 .. 6) {
    my $n = 0;
    try { @s = sort { die "cmp $n\n" if ++$n == $k; $a <=> $b } @s } catch ($e) { print $e }
}
say "@s";
try { my @g = grep { die "grep\n" if $_ > 4; 1 } @s } catch ($e) { print $e; push @s, 9 }
say "@s";
