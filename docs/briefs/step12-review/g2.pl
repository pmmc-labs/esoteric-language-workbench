use v5.42;
# G2: delete, and an assignment to the whole hash, are changes for D76.
# perl reads what is no longer there. (The last line is not run: perl
# 5.42 segfaults on  $h{a} .= (%h = (b => 2)) ? "x" : "y";  )
sub show(%x) { return join ",", map { "$_=$x{$_}" } sort keys %x }
my %h = (a => 1);
sub del() { delete $h{a}; return 0 }
sub clr() { %h = (); return 0 }
my @l = (%h, del());            say "@l";
%h = (a => 1); @l = ($h{a}, del());  say "@l";
%h = (a => 1); @l = (values(%h), clr()); say "@l";
%h = (a => 1); say $h{a} + clr();
%h = (a => 1); $h{a} += delete $h{a};  say "[", show(%h), "]";
%h = (a => 1); @l = ($h{a}, delete $h{a}); say "@l";
