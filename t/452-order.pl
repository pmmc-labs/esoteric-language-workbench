# The order each new form works its parts out in, which is perl's (D80,
# T158, T159, T163): a sub that prints as it is called stands in each
# place. Most are left to right as written. Three are not: `=` to an
# element works out its right side and then its index; an assigning
# operator its index and then its right side; a slice of a list its
# indexes and then its list.
use v5.42;
sub p($v) {
    print "<", $v, ">";
    return $v;
}
my @a = (10, 20, 30, 40);
my @r;

$a[p(1)] = p(5);
say " element =";
$a[p(1)] += p(5);
say " element +=";
$a[p(2)] ||= p(5);
say " element ||=";
$a[p(3)] //= p(5);
say " element //=";
my $v = $a[p(0)] + $a[p(1)];
say " two elements";
@r = (p(1), p(2), p(3));
say " a list";
@r = (p(1) .. p(3));
say " a range";
@r = (p(1), p(2)) x p(2);
say " a list repeated";
@r = @a[p(0), p(2)];
say " a slice";
@r = (p(10), p(20), p(30))[p(0), p(2)];
say " a slice of a list";
say((p(10), p(20))[p(1)]);
@r = splice(@a, p(1), p(1), p(7), p(8));
say " splice";
push @a, p(1), p(2);
say " push";
unshift(@a, p(1), p(2));
say " unshift";
($a[p(0)], $a[p(1)]) = (p(5), p(6));
say " a list assignment";
my ($x, $y) = (p(1), p(2));
say " a list assignment to variables";
say p(1), p(2), " say's list";
$a[p(0)]++;
say " a step";
sub two($q, $w = p("default")) { return $q; }
$v = two(p(1));
say " arguments, then a default";
$v = two(p(1), p(2));
say " two arguments";
