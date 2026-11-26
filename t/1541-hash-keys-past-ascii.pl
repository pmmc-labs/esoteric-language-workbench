# Keys past ASCII, by hand, with perl's answers: a key is its characters,
# whatever they are, and the word before => may not hold one (it is no word
# of the language: T73), so such a key is in quotes.
use v5.42;
use utf8;
use open ':std', ':encoding(UTF-8)';
my %h = ("é" => 1, "e" => 2, "日本" => 3, "☺" => 4, "\x{1F600}" => 5, "e\x{301}" => 6);
say scalar(%h), "|", join(",", map { $_ . "=" . $h{$_} } sort keys %h);
say $h{"é"}, $h{"\x{e9}"}, $h{"日" . "本"}, $h{chr(0x263A)}, exists $h{"E"} ? "E" : "no E", exists $h{"\x{1F600}"} ? "face" : "no face";
$h{"é"} += 10;
$h{lc("Z") . "ü"} = 7;
delete $h{"☺"};
say join(",", map { length($_) . ":" . $_ . "=" . $h{$_} } sort keys %h);
my %long = ("k" x 300 => "long", "" => "empty", " " => "blank", "\n" => "line", "\0" => "nul");
say join(",", map { length($_) . "=" . $long{$_} } sort keys %long);
say $long{"k" x 300}, $long{""}, $long{" "}, $long{"\n"}, $long{"\0"}, exists $long{"k" x 299} ? "short" : "no short";
