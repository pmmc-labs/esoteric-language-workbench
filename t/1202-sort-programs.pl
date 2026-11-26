# sort, by hand, with perl's answers: what the model of step 10c does not
# write.
use v5.42;

my @n = (10, 9, 2, 33, 100, 1);
my @w = ("pear", "Fig", "apple", "fig", "kiwi", "date");

# Without brackets, to the end of the list; one after another.
say join ",", sort @n;
say join ",", sort { $a <=> $b } @n;
say join ",", reverse sort { $a <=> $b } @n;
say join ",", sort { $b <=> $a } grep { $_ > 2 } @n;
say join ",", sort map { $_ * 2 } @n;
say join ",", map { $_ * 2 } sort { $a <=> $b } @n;
say join ",", sort @n, 0, 5;
say join ",", sort +3, 1, 2;
say join ",", sort "b", "a", "c";
say join ",", sort -1, -2, 10;
say join ",", sort { $a <=> $b } -1, -2, 10;

# The first three, and the last.
my @top = (sort { $b <=> $a } @n)[0 .. 2];
say join ",", @top;
my ($least) = sort { $a <=> $b } @n;
say $least;
say((sort { $a <=> $b } @n)[-1]);

# By two keys, with a word operator and with ||; and without regard to
# capitals.
say join " ", sort { length($a) <=> length($b) or $a cmp $b } @w;
say join " ", sort { length($b) <=> length($a) || $b cmp $a } @w;
say join " ", sort { lc($a) cmp lc($b) } @w;

# Stable: the values with one key stay as they were.
say join " ", sort { length($a) <=> length($b) } @w;
say join " ", reverse sort { length($a) <=> length($b) } @w;

# A block of several lines, and of several statements.
my @by_last = sort {
    my $x = substr($a, length($a) - 1, 1);
    my $y = substr($b, length($b) - 1, 1);
    $x cmp $y
} @w;
say join " ", @by_last;

# How many comparisons: perl's own number.
my $count = 0;
my @s = sort { $count++; $a <=> $b } 5, 3, 8, 1, 9, 2, 7;
say $count, " ", join(",", @s);
$count = 0;
@s = sort { $count++; $a <=> $b } 1 .. 20;
say $count;
$count = 0;
@s = sort { $count++; $b <=> $a } 1 .. 20;
say $count;

# In a sub, of what it was handed; and a sub called from the block.
sub sorted(@v) { return sort { $a <=> $b } @v; }
sub key($v) { return $v % 10; }
say join ",", sorted(3, 1, 2), sorted();
say join ",", sort { key($a) <=> key($b) or $a <=> $b } @n;

# In place, and the array is its own again after.
@n = sort { $a <=> $b } @n;
push @n, 0;
@n = sort { $a <=> $b } @n;
say join ",", @n;

# $a[0] in a block is an element of @a, and an array called @a or @b may
# be sorted.
my @a = (3, 1, 2);
my @b = sort { $a <=> $b } @a;
say join ",", @b, sort { $a[0] <=> $a[1] } 5, 4;
