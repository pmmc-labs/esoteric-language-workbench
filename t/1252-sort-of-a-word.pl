# kind: refused
# perl prints true: the word first after sort is a string, or a sub's name (T189).
use v5.42;
my @s = sort true, false;
say @s;
