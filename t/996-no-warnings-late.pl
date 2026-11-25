# kind: refused
# perl takes it anywhere, for the calls written after it in its block (T142).
use v5.42;
say 1;
no warnings 'recursion';
