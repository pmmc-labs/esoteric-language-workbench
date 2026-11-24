# After a number and a blank a dot joins strings, whatever follows it
# (T78, T90): this was refused until step 3 brought the dot.
use v5.42;
say 1.5 .5;
say 1 . .5;
say 1 .5;
