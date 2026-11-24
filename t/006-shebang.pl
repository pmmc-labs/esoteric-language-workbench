#!/usr/bin/perl -n
# kind: refused
# perl takes switches from a first line that starts `#!`: with -n it wraps the
# program in a loop over stdin and, stdin being empty, prints nothing (T72,
# D33). Without the word perl on that line it runs the program named instead.
use v5.42;
say 42;
