# kind: fault
# Brackets round an array with a comma after it are a list of one thing that is a list. By hand.
use v5.42;
my @a = (4, 5, 6);
sub f() {
    return (@a,);
}
say 1;
say f();
my $x = f();
say 2;
