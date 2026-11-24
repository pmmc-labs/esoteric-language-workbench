# check: fails: perl wrote to stderr
# Without `use open`, perl warns of a wide character (D39). Under -CSDA,
# which the oracle once passed, it printed this in silence.
use v5.42;
say "\x{263A}";
