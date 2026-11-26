use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Index {
    field %id_for;
    field $count = 0;
    method register ($key) {
        return $id_for{$key} if exists $id_for{$key};
        my $id = $count++;
        $id_for{$key} = $id;
        return $id;
    }
}
my $ix = Index->new;
print join(",", $ix->register("a"), $ix->register("b"), $ix->register("a"), $ix->register("c")), "\n";
