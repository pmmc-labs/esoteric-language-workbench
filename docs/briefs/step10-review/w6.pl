use v5.42;
# W6: `sort NAME(...)`: a sub's name first after `sort` is the comparator, and its
# brackets are the list. No warning.
sub k() { return 5 }
sub zero(@v) { return 0 }
my @a = (3, 1, 2);
my @r = sort k(), 3, 1;
say "@r";
@r = reverse sort k(), 3, 1;
say "@r";
@r = sort k (3, 1);
say "@r";
@r = sort(k(), 3, 1);          # in sort's own brackets it is a call
say "@r";
@r = sort +k(), 3, 1;
say "@r";
@r = sort { $a <=> $b } k(), 3, 1;
say "@r";
@r = sort zero(@a);          # zero is the comparator, called with no arguments: @a as it was
say "@r";
