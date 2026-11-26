use v5.42;
my @a = (3, 1, 2);
my $count = @a;
my @copy = @a;
my $interp = "@a";
my $last = (4, 5, 6);
my @sorted = sort @a;
my $moved = () = sort @a;
my @kept = (() = sort @a);
my $rev = reverse @a;
my @revd = reverse @a;
my $fields = () = localtime;
my $stamp = localtime;
my $want = wantarray;
my $who = caller;
my @frame = caller;
my @mapped = map { $_ } @a;
my $mapcount = map { $_ } @a;
my @kept2 = grep { $_ } @a;
my $grepcount = grep { $_ } @a;
my @ranged = (1 .. scalar(@a));
my @seed = ("az");
my @lettered = ($seed[0] .. "bb");
my @on = (0, 1, 0, 0, 0, 0);
my @off = (0, 0, 0, 0, 1, 0);
my @idx = (0, 1, 2, 3, 4, 5);
my @window = grep { $on[$_] .. $off[$_] } @idx;
my @seen = ($want, $stamp, $who);
print "$count @copy $interp $last @sorted $moved ", scalar(@kept),
    " $rev @revd $fields ", scalar(@seen), " ", scalar(@frame),
    " @mapped $mapcount @kept2 $grepcount",
    " @ranged @lettered @window\n";
