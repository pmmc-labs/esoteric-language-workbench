# A sub with no signature takes any number of arguments, each worked
# out, and sees none of them (D105). To perl they are in @_.
use v5.42;
sub five { return 5; }
say five();
say five(1, 2, 3);
my $n = 0;
sub quiet { 1 }
quiet($n++, $n++);
say $n;
my @a = (1, 2, 3);
say quiet(@a, @a);
sub later_one { return "late" }
say first_one("x");
sub first_one { return later_one(1) . "!" }
sub none { }
my @r = (none(7), "end");
say scalar(@r);
