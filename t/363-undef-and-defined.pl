# undef, bare only where perl can't take what follows for its argument
# (D48), and defined.
use v5.42;
say undef // 1;
say undef || 2;
say "[" . (defined(undef && 3) ? "d" : "u") . "]";
say undef ? 3 : 4;
say 1 ? 5 : undef;
say defined(1 ? undef : 2) ? "d" : "u";
say defined undef ? "d" : "u";
say defined(undef) ? "d" : "u";
say defined (undef) ? "d" : "u";
say defined((undef)) ? "d" : "u";
say "[" . defined(undef) . "]";
say "[" . (defined undef) . "]";
say defined 1;
say defined "";
say defined 0;
say defined false;
say defined true;
say defined !1;
say defined -1;
say defined "a" . "b";
say "[" . (defined undef // 5) . "]";
say defined(undef) || 5;
say !undef;
say ! defined undef;
say "[" . (!!undef) . "]";
say "[" . (not undef) . "]";

say((undef) // 6);
say undef
    // 7;
say undef # a comment
    || 8;
say undef // undef // 9;
say undef || undef || 10;
say defined(undef // undef) ? "d" : "u";
say defined(length undef) ? "d" : "u";
say defined(length(undef)) ? "d" : "u";
say length(undef) // "no length";
say defined length "" ? "d" : "u";
say substr("abc", undef // 1);
say(undef or 11);
say(undef xor 1);
say "[" . (undef and 1 or 12) . "]";
