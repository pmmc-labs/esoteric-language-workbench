# A program that never ends: t/run.sh must kill it and fail the test
# (t/harness/run.test.ts). Not one of the golden tests: no glob finds it.
use v5.42;
say "before";
while (1) { }
