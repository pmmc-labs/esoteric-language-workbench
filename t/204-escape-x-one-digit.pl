# kind: refused
# perl warns `Non-hex character ' ' terminates \x early`: one digit is enough for it
# only at the end of the string.
use v5.42;
say "\x4 ";
