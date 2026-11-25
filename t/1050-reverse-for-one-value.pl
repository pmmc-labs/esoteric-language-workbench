# kind: refused
# perl: dcba, the arguments joined and their characters reversed (T178, D84).
use v5.42;
my $r = reverse("ab", "cd");
say $r;
