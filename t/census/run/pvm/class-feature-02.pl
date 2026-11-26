use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Foo {
    field $x = 5;
    method m { $x }
}
my $o = Foo->new;
print $o->m, "\n";
