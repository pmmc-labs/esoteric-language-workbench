use v5.42;
# The top of the integers is walked and the loop ends: a counter that steps
# past its end must not.
my $c = 0;
for my $i (9223372036854775805 .. 9223372036854775807) {
    say $i;
    $c++;
    if ($c > 5) { last; }
}
say "done";
