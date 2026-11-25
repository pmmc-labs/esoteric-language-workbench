# ? : groups from the right, and works out one branch.
use v5.42;
say 1 ? 2 : 3;
say 0 ? 2 : 3;
say 0 ? 2 : 3 ? 4 : 5;
say 0 ? 2 : 0 ? 4 : 5;
say 1 ? 2 : 3 ? 4 : 5;
say 1 ? 0 ? "a" : "b" : "c";
say 1 ? 1 ? "a" : "b" : "c";
say 0 ? 1 ? "a" : "b" : "c";
say 1 ? 2 ? 3 ? 4 : 5 : 6 : 7;
say 1 ? "then" : 1 / 0;
say 0 ? 1 / 0 : "else";
say "" ? "t" : "f";
say "0" ? "t" : "f";
say "0.0" ? "t" : "f";
say "a" ? 1 + 1 : 2 + 2;
say 1?2:3;
say 1 ?2 :3;
say 0 ?"a":"b";
say 1 ? .5 : 2;
say 0 ? 1 : .5;
say 1
    ? "over"
    : "lines";
say(1 ? 2 : 3);
say((1 ? 2 : 3) + 1);
say 1 ? (0 ? 1 : 2) : 3;
say "[" . (1 ? "" : "x") . "]";
say length(1 ? "abc" : "");
say 1 ? true : false;
say 2 * (1 ? 3 : 4);
say 1 ? 0 || 5 : 6;
say 0 ? 1 : 0 // 7;
say 1 < 2 ? "less" : "not";
say "a" eq "b" ? "same" : "other";
say 1 ? not 0 : 2;
say 0 ? 2 : not 0;
