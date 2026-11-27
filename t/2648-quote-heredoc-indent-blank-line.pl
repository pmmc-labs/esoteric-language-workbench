# kind: refused
# perl dies: Indentation on line 2 of here-doc doesn't match delimiter.
use v5.42;
print <<~EOT;
    a
  
    EOT
