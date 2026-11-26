use v5.42;
use Time::HiRes qw(time sleep); my $t = time; print $t > 1e9 ? "ok" : "bad", "\n";
