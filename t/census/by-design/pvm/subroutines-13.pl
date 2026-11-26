use v5.42;
sub report {
    my ($x, $y) = @_;
    if ($x > 3) {
        print "both $x $y\n" if $y > 3;
    }
}
report(5, 5);
report(5, 1);
report(1, 5);
