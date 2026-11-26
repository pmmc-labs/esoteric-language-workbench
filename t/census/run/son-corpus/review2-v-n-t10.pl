use v5.42;
sub h { print "h"; return 2 }
sub f { print "a"; return h() + h() }
print f(), "\n";
