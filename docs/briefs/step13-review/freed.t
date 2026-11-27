### for-single-replace
my $r = [1, 2, 3];
for my $x ($r->@*) { $r = [7, 8, 9]; say $x; }
### for-list-replace
my $r = [1, 2, 3];
for my $x ($r->@*, 0) { $r = [7, 8, 9]; say $x; }
### for-braces-list-replace
my $r = [1, 2, 3];
for my $x (@{ $r }, 0) { $r = [7, 8, 9]; say $x; }
### map-replace
my $r = [1, 2, 3];
my @m = map { $r = [7, 8, 9]; $_ * 10 } $r->@*;
say "@m";
### grep-replace
my $r = [1, 2, 3];
my @m = grep { $r = [7, 8, 9]; $_ > 1 } $r->@*;
say "@m";
### sort-replace
my $r = [3, 1, 2];
my @m = sort { $r = [7, 8, 9]; $a <=> $b } $r->@*;
say "@m";
### for-delete-hash
my %h = (l => [1, 2, 3]);
for my $x ($h{l}->@*) { delete $h{l}; say $x; }
### for-delete-hash-list
my %h = (l => [1, 2, 3]);
for my $x ($h{l}->@*, 0) { delete $h{l}; say $x; }
### map-delete-hash
my %h = (l => [1, 2, 3]);
my @m = map { delete $h{l}; $_ * 10 } $h{l}->@*;
say "@m";
### for-hash-clear-list
my %h = (l => [1, 2, 3]);
for my $x ($h{l}->@*, 0) { %h = (); say $x; }
### for-hash-replace-elem
my %h = (l => [1, 2, 3]);
for my $x ($h{l}->@*, 0) { $h{l} = [7, 8, 9]; say $x; }
### for-elem-chain-replace-outer
my $r = [[1, 2]];
for my $x (5, $r->[0][1]) { $r->[0] = [8, 9]; say $x; }
### for-elem-chain-replace-outer2
my $r = [[1, 2]];
for my $x (5, $r->[0][1]) { $r->[0] = [8, 9]; my @junk = map { [$_] } 1 .. 50; say $x; }
### map-values-ref-replace
my $r = {a => 1, b => 2};
my @m = map { $r = {}; $_ * 10 } sort { $a <=> $b } values $r->%*;
say "@m";
### map-values-ref-replace-nosort
my $r = {a => 1};
my @m = map { $r = {z => 5}; $_ * 10 } values $r->%*;
say "@m";
### for-values-ref-replace
my $r = {a => 1, b => 1};
for my $v (values $r->%*) { $r = {}; my @junk = map { [$_] } 1 .. 50; say $v; }
### map-replace-junk
my $r = [1, 2, 3];
my @m = map { $r = [7, 8, 9]; my @junk = map { "j$_" } 1 .. 20; $_ } $r->@*;
say "@m";
### grep-array-of-arrays-replace
my $r = [[1], [2], [3]];
my @m = grep { $r = []; my @j = map { [$_ * 100] } 1 .. 20; $_->[0] > 1 } $r->@*;
say scalar(@m);
