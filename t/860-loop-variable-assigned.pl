# kind: refused
# In perl the loop variable is the element itself: this prints 55 (D17).
use v5.42;
my @a = (1, 2);
for my $x (@a) {
    $x = 5;
}
say @a;
