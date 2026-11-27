# kind: refused
# perl dies: Indentation on line 2 of here-doc doesn't match delimiter (T263).
use v5.42;
print <<~EOT;
    a
  b
    EOT
