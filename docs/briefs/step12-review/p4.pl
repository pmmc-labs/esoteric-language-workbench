use v5.42;
# P4: words perl does not quote across a line end (with W2). perl stops
# compiling at `dump`; `__END__` and `__DATA__` end the program's text.
my %h = (
    dump
        => 1,
);
say join ",", sort keys %h;
