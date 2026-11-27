# kind: refused
# perl: Can't find string terminator "EOT" anywhere before EOF: without ~ the line is EOT alone.
use v5.42;
print <<EOT;
a
  EOT
