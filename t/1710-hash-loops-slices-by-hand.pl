# What stands on a hash, by hand, with perl's answers: what the model of
# step 12b does not reach. Small programs with loops over a hash, slices
# on both sides, a hash as a last parameter, and elements in strings.
use v5.42;

my %stock = (apple => 3, pear => 0, fig => 12, plum => 7);

# A total, a count and a filter, each over the values.
my $total = 0;
$total += $_ for sort { $a <=> $b } values %stock;
my @none = grep { $stock{$_} == 0 } sort keys %stock;
my @most = sort { $stock{$b} <=> $stock{$a} or $a cmp $b } keys %stock;
say "total $total, none of: @none, most first: @most";

# In a string: a word and a scalar for the key, and what is text after.
for my $name (sort keys %stock) {
    say "$name: $stock{$name} left";
}
my $k = "fig";
say "$stock{fig}/$stock{$k} $stock{plum}% $stock{apple}->x $stock{apple}::y $stock{apple}(z) [$stock{pear}] {$stock{fig}}";
say "%stock is text, and so is $stock{apple} %$stock{apple}";
my $line = "$stock{apple}$stock{pear}$stock{fig}";
say $line, length("$stock{fig}$stock{$k}");

# Slices: read in the order asked, stored, swapped, and deleted.
my @two = @stock{"plum", "apple"};
my ($f, $p) = @stock{"fig", "pear"};
say "@two $f $p";
@stock{"apple", "pear"} = @stock{"pear", "apple"};
@stock{"kiwi", "lime", "date"} = (1, 2);
say join(",", map { $_ . "=" . ($stock{$_} // "undef") } sort keys %stock);
my @names = ("kiwi", "lime");
my @gone = delete @stock{@names, "date"};
say scalar(@gone), ":", join(",", map { $_ // "undef" } @gone), ":", join(",", sort keys %stock);
delete @stock{"nope", "fig"};
say join(",", @stock{sort keys %stock});

# A copy by slices, and an array's slice on the left.
my %copy;
@copy{sort keys %stock} = @stock{sort keys %stock};
say join(",", map { $_ . "=" . $copy{$_} } sort keys %copy);
my @row = (0) x 5;
@row[1, 3] = ("b", "d");
@row[0, 4] = @row[4, 0];
@row[5 .. 7] = (5, 6);
say join(",", map { $_ // "undef" } @row);
my @idx = (0, 1);
@row[@idx, 2] = ("x", "y", "z");
say "@row[0 .. 3]";

# A hash as the last parameter: options with defaults.
sub box($text, %opt) {
    my %o = (left => "[", right => "]", times => 1, %opt);
    return $o{left} . $text x $o{times} . $o{right};
}
say box("a"), box("b", times => 2), box("c", left => "<", right => ">"), box("d", (times => 3), left => "(");
sub count_of($x, %) { return $x }
sub keys_of(%o) { return join(",", sort keys %o) }
my %more = (z => 1, y => 2);
say count_of(1, a => 2), keys_of(), keys_of(%more), keys_of(%more, x => 3, %stock);

# The freeze is given back by every way out of a loop.
my %f = (a => 1, b => 2, c => 3, d => 4);
for my $v (sort { $a <=> $b } values %f) { last if $v == 2; }
$f{e} = 5;
OUTER: for my $v (@f{"a", "b"}) { for my $w ($f{c}) { next OUTER; } }
delete $f{a};
my @doubled = map { $_ * 2 } sort { $a <=> $b } values %f;
$f{f} = 6;
sub first_big() { for my $v (sort { $a <=> $b } values %f) { return $v if $v > 3; } return 0; }
say first_big(), "@doubled", scalar(%f);
$f{g} = 7;

# A loop over the keys may change the hash, and one over a count too.
for my $key (sort keys %f) { delete $f{$key} if $f{$key} % 2; $f{uc($key)} = 1; }
for my $i (1 .. scalar(keys %f)) { $f{"n$i"} = $i; }
say join(",", map { $_ . "=" . $f{$_} } sort keys %f);

# A string is a copy: a hash's element in one, in a loop's list, freezes
# nothing.
for my $s ("$f{b}-$f{d}", "x") { $f{b}++; $f{new} = $s; }
say $f{b}, $f{new};

# Reading a frozen hash is no change: elements, exists, a count, a slice.
for my $v (@f{"b", "d"}) {
    say $v + $f{b}, exists $f{zz} ? "zz" : "-", scalar(%f), join("", @f{"d", "b"});
}
