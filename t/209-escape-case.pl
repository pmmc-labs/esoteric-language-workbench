# kind: refused
# perl prints ABC: the case escapes come with interpolation (D43).
use v5.42;
say "\Uabc\E";
