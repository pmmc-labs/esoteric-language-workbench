use v5.42;
print eval { 1 } ? "t" : "f", (eval { die "x\n" } or "caught"), (eval { 0 } // "undef"), "\n";
