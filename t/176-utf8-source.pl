# A source with characters past ASCII (D24): `use utf8;` on a line before
# the first of them (T73), in a comment too; and `use open` to print one
# (D39).
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
# café
say "café";
say 'naïve ☺ 😀';
say length "café";
say length "☺";
say length "😀";
say ord "é";
say ord "☺";
say ord "😀";
say substr("naïve ☺ 😀", 2, 5);
say index("naïve ☺ 😀", "😀");
say "é" x 3;
say "é" . "☺";
say "\x{e9}" . "é"; # é again
say "a
é
b";
