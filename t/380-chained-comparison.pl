# kind: refused
# perl chains it, `1 < 5 && 5 < 3`, and prints n; read from the left it is y (T33, D50).
use v5.42;
say 1 < 5 < 3 ? "y" : "n";
