# check: fails: may not set perl's own variables
# env: PERL_HASH_SEED=0
# The test's environment is perl's too, and this would turn the seeds off.
use v5.42;
my %h = map { $_ => 1 } 1 .. 20;
say join ",", sort { 0 } keys %h;
