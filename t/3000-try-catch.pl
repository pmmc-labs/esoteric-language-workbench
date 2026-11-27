# try and catch, at the top of the file and in a sub (D143): $e is the message,
# with its place; a catch's variable is its own; empty blocks.
use v5.42;
try { die "plain" } catch ($e) { print "1: $e" }
try { die "with newline\n" } catch ($e) { print "2: $e" }
try { say "no die" } catch ($e) { say "not here" }
try { } catch ($e) { say "not here either" }
try { die "ignored\n" } catch ($e) { }
sub safe($n) {
    try {
        return 10 / $n if $n > 1;
        die "too small: $n\n";
    } catch ($e) {
        print "caught ", $e;
        return 0;
    }
}
say safe(5), " ", safe(1);
my $e = "outer";
try { die "x\n" } catch ($e) { my $e = "inner"; say $e }
try { die "y\n" } catch ($e) { $e = "changed"; say $e }
say $e;
sub whine() { die "from a sub" }
try { whine() } catch ($err) { print "3: $err" }
my $x = 0;
my $v = 1;
try { $v = $x // die "undef\n"; say "v is $v" } catch ($e) { print $e }
try { my $w = !die("not") } catch ($e) { print $e }
say "end";
