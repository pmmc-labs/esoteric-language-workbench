# length, uc, lc, ord and chr are perl's named unary operators (D41):
# brackets hold the argument, and without them it is everything that
# binds tighter, which is all of arithmetic and the dot (T87).
use v5.42;
say length "abc";
say length("abc");
say length ("abc");
say length "abc" . "de";
say length("abc") . "de";
say length ("abc") . "de";
say length "ab" x 3;
say length("ab") x 3;
say 1 + length "ab";
say 2 * length "ab" x 3;
say 2 * length("ab") x 3;
say - length "ab";
say -length "ab";
say length -5;
say length -"5";
say length +"ab";
say length +5;
say length(- 5);
say length
    -5;
say length .5;
say length 10 / 4;
say length 2 ** 10;
say length 1 + 1 . 1;
say uc lc "MiXed";
say lc uc "MiXed";
say uc "ab" . lc "CD";
say ord chr 65;
say chr ord "A";
say chr 65;
say chr 65 + 1;
say chr(65) . "x";
say ord "abc";
say ord("abc") + 1;
say ord "a" . "b";
say length(1) + length 22;
say length(length(length "abcdefghij"));
say length length length "abcdefghij";
say length
    "over lines";
say(length "abc");
say((length "abc") + 1);
say "a" . length "bcd";
say "a" x length "bcd";
say substr("abcdef", length "ab");
say substr("abcdef", length "ab", ord chr 2);
say index("abcdef", lc "D");
say uc(substr("abcdef", 1, 3));
say substr ("abcdef", 2);
say substr
    ("abcdef", 3);
say index(
    "abcdef",
    "e"
);
