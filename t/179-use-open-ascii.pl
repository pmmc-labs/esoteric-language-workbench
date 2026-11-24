# A program may build a character past ASCII without `use open`, if it
# doesn't print one.
use v5.42;
say length "\x{e9}";
say ord chr 233;
say length("\x{263A}" x 3);
say uc "plain";
