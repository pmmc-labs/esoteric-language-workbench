use v5.42;
local $SIG{__WARN__} = sub { print "W:$_[0]" }; warn "x\n"; print "end\n";
