# kind: refused
# perl builds the surrogate in silence, and warns when it is printed (T88, D42).
use v5.42;
say length "\x{D800}";
