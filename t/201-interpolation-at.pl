# kind: refused
# perl doesn't compile this one: `@example` is an array to it (T34).
use v5.42;
say "user@example.com";
