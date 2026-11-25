# kind: refused
# perl compiles this, and not with the call before the sub: v65 is a version string (T136).
use v5.42;
sub v65() { return 1; }
say v65();
