use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Base {
    field $trail = "";
    ADJUST { $trail .= "b" }
    method mark ($c) { $trail .= $c; return }
    method trail { return $trail }
}
class Derived :isa(Base) {
    ADJUST { $self->mark("d") }
}
print Derived->new->trail, "\n";
