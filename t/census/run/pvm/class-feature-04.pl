use v5.42;
use feature 'class';
no warnings 'experimental::class';
class Flags { field $quiet :param :reader = !!0; field $loud :param :reader = !!1; }
my $f = Flags->new;
print $f->quiet ? "q" : "-", $f->loud ? "l" : "-", Flags->new(quiet => 1)->quiet ? "Q" : "-", "\n";
