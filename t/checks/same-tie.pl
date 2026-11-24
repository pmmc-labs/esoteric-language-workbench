# check: fails: changes from run to run
# A real sort, with a tie in it: pine and elm both come to 7, and perl's
# sort keeps them in the hash's order. Reading can't see that.
use v5.42;
my %count;
$count{$_}++ for qw(kiwi yam elm elm pine pine pine pine elm kiwi pine elm plum elm plum elm yam yam yam pine elm apple kiwi pine);
for my $word (sort { $count{$b} <=> $count{$a} } keys %count) {
    say "$word: $count{$word}";
}
