use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Foo {
    field $x = 1;
    ADJUST { $x = 2 }
}
print ref(Foo->new), "\n";
