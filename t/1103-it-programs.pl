# $_, the two fors, map and grep, by hand, with perl's answers: what the
# model of step 10b does not write.
use v5.42;

# Without brackets, to the end of the list they stand in; one after another.
my @a = (3, 1, 4, 1, 5);
say join ",", map { $_ * 2 } grep { $_ > 1 } @a;
my @r = (9, map { $_ + 1 } @a, 9);
say join ",", @r;
my @s = (map { $_ } 1, 2);
say @s;
say join "", reverse map { $_ * $_ } 1 .. 4;

# The modifier with a bare list, and each statement it may follow.
my $n = 0;
$n += $_ for 1, 2, 3;
say $n;
my @b;
push @b, $_ * 2 for (1, 2), 3;
say @b;
print $_ for 1 .. 3;
print "\n";
say "v", $_ for @b;
say 1 for ();

# Counting, testing, and choosing.
my $big = grep { $_ > 2 } @a;
my $pairs = map { ($_, $_) } @a;
say $big, " ", $pairs;
say "has a four" if grep { $_ == 4 } @a;
say "has no nine" unless grep { $_ == 9 } @a;
my ($first) = grep { $_ > 3 } @a;
say $first;

# Blocks: a unary minus first, brackets first, a not, a plus, a string
# that is not followed by a comma, a my, and two tests joined by a word.
say join ",", map { -$_ } @a;
say join ",", map { ($_, 0) } 1, 2;
say join ",", map { !$_ } 1, 2;
say join ",", map { +$_ } @a;
say join ",", map { "<" . $_ . ">" } @a;
say join ",", map { my $q = $_ * 3 } @a;
say join ",", map { $_ > 1 or 0 } @a;
say join ",", grep { $_ > 1 and $_ < 5 } @a;
say join ",", map { ($_) x 2 } 1, 2;

# A loop inside a block, with a next and a last of its own.
say join ",", map {
    my $t = 0;
    for my $i (1, 2, 3) {
        next if $i == 2;
        last if $i == 3;
        $t += $i;
    }
    $t + $_
} 10, 20;

# A block over several lines: each statement on its own.
my @words = ("pear", "fig", "apple");
my @lens = map {
    my $w = $_;
    my $l = length($w);
    $l > 3 ? ($w, $l) : ()
} @words;
say join " ", @lens;

# $_ in a for, an inner for's $_, and a my of the outer one.
for (@words) {
    my $w = $_;
    for (1, 2) {
        print $w, $_, " ";
    }
    print $_, "\n";
}

# A sub that maps what it was given, and one that greps the file's array.
sub doubled(@v) { return map { $_ * 2 } @v; }
sub over($least) { return grep { $_ > $least } @a; }
say join ",", doubled(over(2)), doubled();

# As statements, for what the block does: perl does not warn.
map { push @b, $_ } 7, 8;
grep { push @b, $_ } 9;
say scalar(@b);

# The array is given back after each: changed between two maps of it.
@a = map { $_ + 1 } @a;
push @a, 0;
@a = grep { $_ } @a;
say join ",", @a;

# In the first part of a for of three parts, after a my: the grep runs
# when the first my has its value already. And a block with a `;` in a
# for's list.
sub counted() {
    for (my $i = 0, my $c = grep { $_ > 1 } @a; $i < $c; $i++) {
        print $i;
    }
    print "\n";
    return 0;
}
counted();
for (map { my $t = $_; $t * 2 } 1, 2, 3) {
    print $_;
}
print "\n";
