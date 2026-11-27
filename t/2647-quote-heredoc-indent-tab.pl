# kind: refused
# perl dies: Indentation on line 1 of here-doc doesn't match delimiter (T263).
use v5.42;
print <<~EOT;
	a
    EOT
