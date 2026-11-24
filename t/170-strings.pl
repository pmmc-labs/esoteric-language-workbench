# String literals of both kinds (D43).
use v5.42;
say "hello";
say 'hello';
say "";
say '';
say "a" . 'b';
say "it's";
say 'say "hi"';
say "say \"hi\"";
say 'it\'s';
say 'a\\b';
say 'a\nb';
say 'a\b\q\x41';
say '$x @y %z';
say "\$x \@y %z";
say "a # not a comment";
say 'a # not a comment'; # a comment
say "two
lines";
say 'two
lines';
say "	a tab";
say("brackets");
say ("a blank and brackets");
say(("a") . ("b"));
