# check: ok
# stdin: one\ntwo\n
# args: left right
# env: CURLY_CHECK=set
# perl is given the test's stdin, arguments and environment, as the
# compiled program is by t/run.sh.
use v5.42;
my @lines = <STDIN>;
print "stdin: $_" for @lines;
say "args: @ARGV";
say "env: $ENV{CURLY_CHECK}";
