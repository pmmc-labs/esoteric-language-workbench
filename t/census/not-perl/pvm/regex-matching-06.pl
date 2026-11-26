use v5.42;
use v5.36;
sub token_end ($input, $position, $pattern) {
    pos($input) = $position;
    return $input =~ /\G($pattern)/ ? $position + length($1) : undef;
}
print token_end("aab", 1, "a+"), " ", token_end("aab", 2, "b"), " ",
      defined token_end("aab", 0, "b") ? "matched" : "none", "\n";
