# kind: refused
# perl dies: Can't use string ('2') as an ARRAY ref while 'strict refs' in use.
use v5.42;
say((1, 2)->[0]);
