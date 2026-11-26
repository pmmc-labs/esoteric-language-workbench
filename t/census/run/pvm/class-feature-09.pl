use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Registry {
    field %classes;
    method add ($name) { $classes{$name} = 1; return $self }
    method classes { return values %classes }
}
my $r = Registry->new->add("A")->add("B");
my @all = $r->classes;
my $n = $r->classes;
print scalar(@all), " $n\n";
