# kind: refused
# perl runs out of memory as it compiles (T271).
use v5.42;
say sprintf("%99999999999d", 1);
