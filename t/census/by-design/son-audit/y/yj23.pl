use v5.42;
our $v = "main"; package P; our $v = "p"; package main; print $v, $main::v, $P::v, "\n";
