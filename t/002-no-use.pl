# kind: refused
# A program begins `use v5.42;` (D16): without it the file means something
# else to perl, which has no `say` until the line turns it on.
say 42;
