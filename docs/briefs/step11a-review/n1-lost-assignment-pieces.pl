use v5.42;
# N1: T129 says a concatenation of three pieces is assigned.  A string is not:
# every string of two pieces or more loses the assignment.
my ($t, $u, $x, $z, @a);
sub reset_() { $t = "t"; $u = "u"; $x = "a"; $z = "z"; @a = (1, 2); }
reset_(); $t .= ($u = "$x$z$x");     say "01 $t $u";
reset_(); $t .= ($u = "$x-$z");      say "02 $t $u";
reset_(); $t .= ($u = "-$x-");       say "03 $t $u";
reset_(); $t .= ($u = "$x$z$x$z");   say "04 $t $u";
reset_(); $t .= ($u = "$x$a[0]@a");  say "05 $t $u";
reset_(); $t .= ($u = "@a@a");       say "06 $t $u";
reset_(); $t .= ($u = "@a-@a");      say "07 $t $u";
reset_(); $t .= ($u = $x . $z . $x); say "08 $t $u";    # T129's: assigned
