# kind: warns
# say STDERR and print STDERR (15b): a list, each value as say has it.
use v5.42;
my @a = (1, 2, 3);
my %h = (k => "v");
print STDERR "one ", "two\n";
say STDERR @a;
say STDERR "count: ", scalar(@a), " $h{k}";
say "on stdout";
print STDERR 1.5, " ", 10 / 4, "\n";
say STDERR "x" if @a;
say STDERR $_ for @a;
