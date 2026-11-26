use v5.42;
our $name = "widget";
our $qty  = 7;
format STDOUT =
@<<<<<<< @>>>
$name,   $qty
.
write;
print "after write\n";
