# kind: refused
# perl takes it, as a sub at the top (T31).
use v5.42;
{
    sub inner() { return 1; }
}
say inner();
