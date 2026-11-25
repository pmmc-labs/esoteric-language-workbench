# kind: refused
# perl doesn't compile it: `or` binds more loosely than the commas, and takes the list
# before it for its left side.
use v5.42;
say index("abcabc", "c", 0 or 3);
