# kind: fault
# perl gives -1 or 0 by whether the string is UTF-8 inside (T281).
use v5.42;
say rindex("abc", "a", 9223372036854775806);
say rindex("abc", "a", 9223372036854775807);
