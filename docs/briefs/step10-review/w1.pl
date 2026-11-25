use v5.42;
# W1: grep, sort and reverse hand on the containers of their list (map and join do not).
# A later part of the same list, expression or argument list changes one, and perl shows the change.
my @a = (1, 2, 3);
sub chg() { $a[0] = 50; return 7 }
my $v = 1;
sub bump() { $v = 9; return 5 }
my @r;
@r = (reverse(@a), chg());                       say "reverse: @r"; @a = (1, 2, 3);
@r = ((grep { 1 } @a), chg());                   say "grep:    @r"; @a = (1, 2, 3);
@r = ((sort { $a <=> $b } @a), chg());           say "sort:    @r"; @a = (1, 2, 3);
@r = ((sort @a), chg());                         say "sort2:   @r"; @a = (1, 2, 3);
@r = ((map { $_ } @a), chg());                   say "map:     @r"; @a = (1, 2, 3);
@r = ((grep { 1 } $v), bump());                  say "scalar:  @r"; $v = 1;
@r = (reverse($v, 0), bump());                   say "scalar2: @r"; $v = 1;
say "slice:   ", (reverse(@a))[2] + chg();       @a = (1, 2, 3);
say "slice2:  ", (grep { 1 } $v)[0] + bump();    $v = 1;
say "say:     ", reverse(@a), chg();             @a = (1, 2, 3);
say "join:    ", join("-", reverse(@a), chg());  @a = (1, 2, 3);
for my $x (reverse(@a), chg()) { print $x } say " :foreach"; @a = (1, 2, 3);
@r = map { $_ } (reverse(@a), chg());            say "inner:   @r"; @a = (1, 2, 3);
sub f($p //= bump(), $q = 0) { return "$p/$q" }
say "default: ", f(undef, grep { 1 } $v);        $v = 1;
say "default2: ", f(undef, reverse($v));         $v = 1;
