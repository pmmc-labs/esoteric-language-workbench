use v5.42;
# W2: `v` and digits before `=>`, with a line end between. The proposal:
# "`=>` quotes across the end of a line and a comment", "whatever the
# word" (T214 has `v65 => 8` on one line, which is the key `v65`).
my %h = (
    v65 => 1,
    v66
        => 2,
    v67    # a comment
        => 3,
);
say join ",", sort keys %h;
