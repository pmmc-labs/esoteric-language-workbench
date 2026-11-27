# kind: refused
# perl does not compile it: Can't find string terminator '"' anywhere before EOF (T264).
use v5.42;
say <<EOT . "a
b";
c
EOT
