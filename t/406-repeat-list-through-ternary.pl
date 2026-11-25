# And both branches of ? : (T104). A list from step 9; until then this
# test was of its refusal.
use v5.42;
say(1 ? ("a") x 3 : "b");
say(0 ? "b" : ("a", "c") x 2);
