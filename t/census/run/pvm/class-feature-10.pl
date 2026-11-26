use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Holder {
    field %registry;
    field @order;
    method register ($graphs) { %registry = $graphs->%*; @order = sort keys %registry; return $self }
    method clear { @order = (); return $self }
    method summary { return scalar(keys %registry) . ":" . join(",", @order) }
}
my $h = Holder->new->register({ b => 2, a => 1 });
print $h->summary, " ", $h->clear->summary, "\n";
