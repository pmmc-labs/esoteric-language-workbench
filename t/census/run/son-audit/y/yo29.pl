use v5.42;
use Cwd qw(getcwd); print getcwd() =~ m{^/} ? "abs" : "rel", "\n";
