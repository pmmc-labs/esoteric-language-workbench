use v5.42;
my $show = sub { return "[@_]" };
sub outer { return "amp=" . &$show . " paren=" . &$show(); }
print outer("x", "y"), "\n";
print $show->(), "\n";
