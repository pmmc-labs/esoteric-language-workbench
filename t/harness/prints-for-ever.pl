# A program that prints without end: t/run.sh must stop it at its limit
# and fail the test, long before the watchdog would (t/harness/run.test.ts).
use v5.42;
while (1) { say "a line of output, again and again and again"; }
