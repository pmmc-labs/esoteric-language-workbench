# perl takes the last statement of a block without its semicolon, and
# from step 8 so does the language (D75). Until then this test was of
# its refusal.
use v5.42;
if (1) {
    say 1
}
