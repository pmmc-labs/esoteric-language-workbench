use v5.42;
package C; sub get { my $c=shift; bless {n=>0}, $c } package main; print C->get->{n},"\n";
