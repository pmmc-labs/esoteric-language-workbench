use v5.42;
# P3: what follows a hash's element in a string. Step 11a's list refuses
# `{`, "a second `[`", `::` and `->` before `[ { @ $` after a variable;
# after `$h{a}` the first `[` is an index already. perl dies at the first
# say; each of the others alone dies the same way.
my %h = (a => 1);
say "$h{a}->%*|$h{a}->|$h{a}::x|$h{a}(0)";      # text, in silence
say "$h{a}[0]";
say "$h{a}->[0]";
say "$h{a}->{b}";
say "$h{a}->@*";
say "$h{a}->$*";
