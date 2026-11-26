use v5.42;
my $calls = 0;
sub helper { $calls++ }
sub f {
    my ($x, $y) = @_;
    if ($x > 3) {
        helper() if $y > 3;
    }
}
f(5, 5); f(5, 1); f(1, 5);
print "$calls\n";
