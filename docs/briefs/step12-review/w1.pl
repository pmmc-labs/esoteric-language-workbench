use v5.42;
# W1: one word alone in the braces, with a line end or a comment beside it.
# The proposal: "One word alone in the braces is that string, whatever the
# word." perl: only when nothing but blanks and tabs stands between the
# braces and the word, on one line.
my %h;
$h{
    true
} = "a";
$h{ true } = "b";
$h{false   # the flag
} = "c";
$h{
    v65 } = "d";
$h{ v65 } = "e";
say join ",", map { "[$_]=$h{$_}" } sort keys %h;
my %g = (1 => "one", true => "the word");
say $g{ true };
say $g{
    true
};
