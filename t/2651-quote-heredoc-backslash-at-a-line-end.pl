# kind: refused
# perl takes the backslash away: a and b on two lines. A backslash before a new line is refused everywhere (D43).
use v5.42;
print <<"EOT";
a\
b
EOT
