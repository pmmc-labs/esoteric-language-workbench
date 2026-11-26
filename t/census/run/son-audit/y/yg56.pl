use v5.42;
my $s="abcabc"; print index($s,"c"), index($s,"c",3), index($s,"z"), rindex($s,"b"), rindex($s,"b",3), index($s,""), rindex($s,""), "\n";
