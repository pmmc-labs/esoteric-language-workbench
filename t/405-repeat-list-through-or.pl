# perl repeats a list here too: the list that say's argument is reaches
# the right of `||` (T104). A list from step 9; until then this test was
# of its refusal.
use v5.42;
say(0 || ("a") x 3);
say(0 || ("a", "b") x 2);
