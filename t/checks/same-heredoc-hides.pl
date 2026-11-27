# check: fails: line 10: keys without sort
# An apostrophe in a heredoc: a reader that paired it with the next
# quote would hide the unsorted keys after the body (step 16a).
use v5.42;
my %h = (a => 1);
print <<'EOT';
it's here
EOT
say "x";
say join ",", keys %h;
