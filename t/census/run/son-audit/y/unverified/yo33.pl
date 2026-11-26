use v5.42;
use Text::Balanced qw(extract_bracketed); my ($ext, $rem) = extract_bracketed("(a (b) c) rest", "()"); print "$ext|$rem\n";
