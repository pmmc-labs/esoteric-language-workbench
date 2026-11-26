use v5.42;
format STDOUT =
a report line
.

my $shell = qx{echo hi};
my $here = <<"EOT";
heredoc line
EOT

=pod

Prose the lexer eats and the optree never sees.

=cut

my @none = <*.nonexistent-xyz>;
my @data = <DATA>;
print $shell, $here, "glob ", scalar(@none), "\n";
my $packed = pack("C3", $ENV{X} // 65, 66, 67);
print $packed, " ", unpack("C3", $packed), "\n";
write;
print @data;
__END__
from the data section
