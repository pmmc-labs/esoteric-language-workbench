use v5.42;
# W5: the word first after `sort` is a name to perl, not a value: `true` there is
# the string "true" (toke.c forces a word after sort). No warning without brackets.
my @r = sort true, false;
say join("|", @r);
@r = sort true;
say join("|", @r);
@r = sort false, 3, 2;
say join("|", @r);
@r = sort true . "x", "a";
say join("|", @r);
@r = reverse sort true, false;
say join("|", @r);
@r = sort { $a cmp $b } true, false;     # after a block it is the boolean
say join("|", @r);
@r = sort +true, false;
say join("|", @r);
