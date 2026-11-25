# Loops over lists, by hand, with perl's answers: what the model of step
# 9b does not write.
use v5.42;

# A sum, a largest, and a string built up.
my @n = (3, 1, 4, 1, 5, 9, 2, 6);
my $sum = 0;
my $most = $n[0];
my $all = '';
foreach my $v (@n) {
    $sum += $v;
    $most = $v if $v > $most;
    $all .= $v . ($v == $n[-1] ? '' : ',')
}
say $sum, ' ', $most, ' ', $all;

# Strings, undef, booleans and numbers in one list.
for my $v ('a', undef, true, false, 1.5, -0.0, "") {
    say defined($v) ? '<' . $v . '>' : 'undef';
}

# A copy of the array is another array: the loop is over the copy's
# values, and the first may be changed.
my @copy = @n;
for my $v (@copy) {
    push @n, $v * 2 if $v > 4;
}
say scalar(@n), ' ', $n[-1];

# A sub that walks the file's array, called while a loop is over it: the
# array is frozen twice over, and read.
sub count_above($least) {
    my $c = 0;
    for my $v (@n) {
        $c++ if $v > $least
    }
    return $c;
}
my $line = '';
for my $v (@n[0, 1, 2]) {
    $line .= count_above($v) . ' ';
}
say $line;

# A sub that calls itself from inside its loop.
my @tree = (1, 2, 3);
sub walk($depth) {
    return '.' if $depth == 0;
    my $out = '';
    for my $v (@tree) {
        $out .= $v . walk($depth - 1);
    }
    return $out;
}
say walk(2);
push @tree, 4;
say scalar(@tree);

# The loop's variable shadows one outside, and a my in the block shadows
# the loop's.
my $v = 'outside';
for my $v (1, 2) {
    my $w = $v;
    {
        my $v = $w * 10;
        say $v;
    }
}
say $v;
# The list is read before the loop's variable is: its $v is the one outside.
for my $v ($v . '!', length($v)) {
    say $v;
}

# Elements and a slice that are there, through what hands a list on.
my @e = (10, 20, 30);
for my $x (1 ? $e[2] : 0, 0 || $e[1], +$e[0], ($e[0]) x 2, @e[2, 0], $e[5] // 'none', $e[7] || 'no') {
    print $x, ' ';
}
say scalar(@e);

# Building one array from another, both ways.
my @squares;
for my $i (1 .. 5) {
    push @squares, $i * $i;
}
my @back;
for my $s (@squares) {
    unshift @back, $s;
}
say $squares[0], ' ', $squares[4], ' ', $back[0], ' ', $back[4];

# A labelled search of two lists.
my @xs = (1, 2, 3);
my @ys = (4, 5, 6);
my $found = 'none';
PAIR: for my $x (@xs) {
    for my $y (@ys) {
        next PAIR if $y > 5;
        if ($x * $y == 10) {
            $found = $x . '*' . $y;
            last PAIR;
        }
    }
}
say $found;
push @xs, 0;
push @ys, 0;
say scalar(@xs) + scalar(@ys);
