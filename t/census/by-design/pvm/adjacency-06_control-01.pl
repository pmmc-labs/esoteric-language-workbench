use v5.42;
use feature "switch";
my $n = $ENV{N} // 2;
my $r = $ENV{R} // 0;
my @l = ($ENV{A} // "a", "b");
if ($n) { print "if" } else { print "else" }
print "-unless" unless $n;
my $i = 0;
while ($i < $n) { last if $i > 1; print "-w$i"; $i = $i + 1 }
until ($i >= $n + 2) { $i = $i + 1; next if $i > $n + 1; print "-u$i" }
my $k = 0;
do { $k = $k + 1 } while $k < $n;
print "-d$k";
my $v = do { my $t = $n; $t + 1 };
print "-v$v";
my $e = eval { 10 / ($ENV{X} // 0) } // "t";
print "-e$e";
eval { die "x\n" };
print "-D$@";
exit 3 if $r;
print "-X";
my $t = time;
print "-t", $t > 1000000000 ? 1 : 0;
for (my $j = 0; $j < 1; $j = $j + 1) { print "-c$j" }
foreach my $x (@l) { redo if $r; print "-f$x" }
print "-p" if $n;
given ($n) { when (2) { print "-g" } default { print "-G" } }
goto DONE;
print "-skipped";
DONE:
print "\n";
