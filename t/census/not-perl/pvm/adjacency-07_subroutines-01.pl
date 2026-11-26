use v5.42;
use v5.36;
sub pick ($n, $label = "small") {
    return $label if $n < 10;
    for my $i (1 .. 2) {
        next if $i == 1;
        return "big-" . $i;
    }
    return "none";
}
sub bump { $_[0]++ }
sub answer { 42 }
sub f { return "f[" . join("-", @_) . "]" }
no feature "signatures";
sub g ($) { return "g[" . $_[0] . "]" }
use feature "signatures";
my $anon = sub { pick($_[0]) . "/" . &pick($_[1], "tiny") };
my $seen = 0;
bump($seen);
my $n = $seen;
lock($n);
local $SIG{__WARN__} = sub { };
my @greedy = (warn "a", "b");
my @cut = (warn("a"), "b");
print pick(1), " ", pick(50), " ", $anon->(2, 3), " ", $seen, "\n";
print &answer, " ", answer(), " ", answer, "\n";
print scalar @greedy, scalar @cut, "\n";
print f 1, 2;
print "\n";
print g 1, 2;
print "\n";
my $slot = 0;
sub slot :lvalue { $slot }
slot() = answer() + $seen;
print slot(), "\n";
