# check: fails: line 5: a string with code in it
# A string that runs code can hold a hash where the reader doesn't look.
use v5.42;
my %h = (a => 1);
say "stock: @{[ %h ]}";
