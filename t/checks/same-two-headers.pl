# check: fails: more than one `# args:` header
# args: left
# args: right
# t/run.sh would give the program both lines, and the check the last.
use v5.42;
say "@ARGV";
