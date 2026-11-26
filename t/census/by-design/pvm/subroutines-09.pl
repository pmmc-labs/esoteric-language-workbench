use v5.42;
sub check {
    for my $x (@_) {
        die "too big: $x\n" if $x > 1;
    }
    return "ok";
}
print eval { check(1, 0) } // $@, "\n";
print eval { check(1, 9) } // $@;
