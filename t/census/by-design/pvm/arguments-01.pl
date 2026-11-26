use v5.42;
sub describe {
    return $_[0] . "-" . $_[1] . "-" . scalar(@_);
}
print describe("a", "b", "c"), "\n";
