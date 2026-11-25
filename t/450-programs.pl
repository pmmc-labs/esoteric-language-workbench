# Small programs the language can say now, each with an array.
use v5.42;

# The primes below 60, by the sieve.
my @composite;
my @primes;
my $n = 2;
while ($n < 60) {
    unless ($composite[$n]) {
        push @primes, $n;
        my $m = $n * $n;
        while ($m < 60) {
            $composite[$m] = true;
            $m += $n;
        }
    }
    $n++;
}
sub show() {
    my $line = "";
    my $i = 0;
    while ($i < @primes) {
        $line .= " " if $i;
        $line .= $primes[$i];
        $i++;
    }
    return $line;
}
say show();
say scalar(@primes), " primes, the last ", $primes[-1];

# A bubble sort, in place, by swapping elements.
my @v = (5, 3, 8, 1, 9, 2, 7);
my $swapped = true;
while ($swapped) {
    $swapped = false;
    for (my $i = 0; $i < $#v; $i++) {
        if ($v[$i] > $v[$i + 1]) {
            ($v[$i], $v[$i + 1]) = ($v[$i + 1], $v[$i]);
            $swapped = true;
        }
    }
}
say @v;

# A stack and a queue.
my @stack;
push @stack, 1, 2, 3;
my $top = pop(@stack);
push @stack, $top * 10;
say "stack: ", @stack;
my @queue = (1, 2, 3);
push @queue, shift(@queue);
unshift @queue, 0;
say "queue: ", @queue;

# Pascal's triangle, a row from the one before.
my @row = (1);
for (my $r = 0; $r < 6; $r++) {
    say @row[0 .. $#row] if $r < 2;
    my @next = (1);
    for (my $k = 1; $k < @row; $k++) {
        push @next, $row[$k - 1] + $row[$k];
    }
    push @next, 1;
    @row = @next;
}
say $row[3], " ", scalar(@row);

# A moving average of three, with splice for the window.
my @samples = (4, 8, 6, 2, 10, 12);
my @window;
my @averages;
while (@samples) {
    push @window, shift(@samples);
    splice(@window, 0, 1) if @window > 3;
    my $sum = 0;
    for (my $i = 0; $i < @window; $i++) {
        $sum += $window[$i];
    }
    push @averages, $sum / @window if @window == 3;
}
say scalar(@averages), ": ", $averages[0], " ", $averages[1], " ", $averages[2], " ", $averages[3];

# Fibonacci numbers in an array, each from the two before.
my @fib = (0, 1);
push @fib, $fib[-1] + $fib[-2] while @fib < 15;
say $fib[14];

# An array turned round, by swapping from both ends.
my @letters = ("a", "b", "c", "d", "e");
my ($lo, $hi) = (0, $#letters);
while ($lo < $hi) {
    ($letters[$lo], $letters[$hi]) = ($letters[$hi], $letters[$lo]);
    $lo++;
    $hi--;
}
say @letters;

# A binary search, by a sub over the file's array.
my @sorted = (2, 3, 5, 7, 11, 13, 17, 19, 23);
sub find($want) {
    my ($from, $to) = (0, $#sorted);
    while ($from <= $to) {
        my $mid = ($from + $to - ($from + $to) % 2) / 2;
        return $mid if $sorted[$mid] == $want;
        if ($sorted[$mid] < $want) { $from = $mid + 1 } else { $to = $mid - 1 }
    }
    return -1;
}
say find(13), " ", find(2), " ", find(23), " ", find(4);
