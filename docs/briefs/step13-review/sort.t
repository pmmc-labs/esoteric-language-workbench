### inplace-named
my @a; $a[2] = "c"; $a[0] = "a";
@a = sort { (defined $a ? $a : "") cmp (defined $b ? $b : "") } @a;
say scalar(@a);
### inplace-ref-both
my $r = []; $r->[2] = "c"; $r->[0] = "a";
$r->@* = sort { (defined $a ? $a : "") cmp (defined $b ? $b : "") } $r->@*;
say scalar($r->@*);
### inplace-braces-both
my $r = []; $r->[2] = "c"; $r->[0] = "a";
@{ $r } = sort { (defined $a ? $a : "") cmp (defined $b ? $b : "") } @{ $r };
say scalar($r->@*);
### inplace-name-via-ref
my @a; $a[2] = "c"; $a[0] = "a"; my $r = \@a;
@a = sort { (defined $a ? $a : "") cmp (defined $b ? $b : "") } $r->@*;
say scalar(@a);
### inplace-ref-via-name
my @a; $a[2] = "c"; $a[0] = "a"; my $r = \@a;
$r->@* = sort { (defined $a ? $a : "") cmp (defined $b ? $b : "") } @a;
say scalar(@a);
### inplace-two-refs
my $r = []; $r->[2] = "c"; $r->[0] = "a"; my $s = $r;
$r->@* = sort { (defined $a ? $a : "") cmp (defined $b ? $b : "") } $s->@*;
say scalar($r->@*);
### inplace-elem-chain
my %h = (l => []); $h{l}[2] = "c"; $h{l}[0] = "a";
$h{l}->@* = sort { (defined $a ? $a : "") cmp (defined $b ? $b : "") } $h{l}->@*;
say scalar($h{l}->@*);
### inplace-reverse-ref
my $r = []; $r->[2] = "c"; $r->[0] = "a";
$r->@* = reverse $r->@*;
say scalar($r->@*), defined $r->[1] ? "def" : "undef";
### inplace-reverse-named
my @a; $a[2] = "c"; $a[0] = "a";
@a = reverse @a;
say scalar(@a), defined $a[1] ? "def" : "undef";
### inplace-nonblock-ref
my $r = ["b", "a"]; $r->[3] = "c";
$r->@* = sort $r->@*;
say scalar($r->@*);
