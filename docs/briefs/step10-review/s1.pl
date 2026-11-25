use v5.42;
# Shapes perl warns on (D15) that the proposal's rules take in silence. Run for the messages.
my @r;
my @z = ("abc");  @r = sort { $a <=> $b } @z;     # Argument "abc" isn't numeric in sort: one element, no comparison
my @u = (undef);  @r = sort @u;                   # Use of uninitialized value $u[0] in sort
my @w = (undef);  @r = sort { $b cmp $a } @w;     # the same
my @g = (undef);  @r = sort { lc($a) cmp lc($b) } @g;   # silent: a block perl does not optimise away
say join(undef, "a");                             # Use of uninitialized value in join or string: a separator never used
my @a = (3, 1, 2);
@r = (sort (@a), 9);                              # sort (...) interpreted as function
say "@r";
