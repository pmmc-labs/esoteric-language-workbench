# check: ok
# A heredoc, a q() and a qw() whose apostrophes, percents and words the
# reading rule must not take for code (step 16a); the hash is sorted.
use v5.42;
my %h = (b => 2, a => 1);
print <<"EOT";
it's 100% done, keys and all
EOT
say q{it's %h}, qw(keys values);
say join ",", sort keys %h;
