use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Node {
    field $inputs :param;
    field $left :param = undef;
    field $calls = 0;
    ADJUST { $left //= $self->first }
    method first { $calls++; return $inputs->[0] }
    method left { return $left }
    method calls { return $calls }
}
my $a = Node->new(inputs => [7, 8]);
my $b = Node->new(inputs => [7, 8], left => 1);
print join(",", $a->left, $a->calls, $b->left, $b->calls), "\n";
