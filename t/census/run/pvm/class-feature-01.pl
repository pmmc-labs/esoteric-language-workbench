use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Empty {}
print ref(Empty->new), "\n";
