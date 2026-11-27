# model: t/models/die.py
use v5.42;
try { try { try { try { try { die "core" } catch ($e) { die $e } } catch ($e) { die $e } } catch ($e) { die "L2: $e" } } catch ($e) { die "L3: $e" } } catch ($e) { print "top: $e" }
try { try { try { die "core" } catch ($e) { die "L0: $e" } } catch ($e) { die "L1: $e" } } catch ($e) { print "top: $e" }
try { try { try { try { try { die "core" } catch ($e) { die "new0" } } catch ($e) { die $e } } catch ($e) { die "L2: $e" } } catch ($e) { print "L3 kept: $e" } } catch ($e) { print "top: $e" }
try { try { try { try { die "core" } catch ($e) { die "new0" } } catch ($e) { die $e } } catch ($e) { die $e } } catch ($e) { print "top: $e" }
try { try { try { try { die "core" } catch ($e) { die "L0: $e" } } catch ($e) { die "new1" } } catch ($e) { print "L2 kept: $e" } } catch ($e) { print "top: $e" }
try { try { try { try { die "core" } catch ($e) { die "L0: $e" } } catch ($e) { die "new1" } } catch ($e) { print "L2 kept: $e" } } catch ($e) { print "top: $e" }
try { try { try { try { die "core" } catch ($e) { die $e } } catch ($e) { die "new1" } } catch ($e) { die $e } } catch ($e) { print "top: $e" }
try { try { try { die "core" } catch ($e) { die "new0" } } catch ($e) { print "L1 kept: $e" } } catch ($e) { print "top: $e" }
try { try { die "core" } catch ($e) { print "L0 kept: $e" } } catch ($e) { print "top: $e" }
try { try { try { die "core" } catch ($e) { die "L0: $e" } } catch ($e) { print "L1 kept: $e" } } catch ($e) { print "top: $e" }
