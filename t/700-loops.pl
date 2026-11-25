# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $i = 0;
    while ($i < 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    until ($i >= 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while (($i++) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while ((++$i) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    until (($i++) > 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while (($i += 2) < 7) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while (!($i >= 3)) {
        say($i);
        $i++;
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (my $k = 0; $k < 3; $k++) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (my $k = 0; $k < 3; ++$k) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (; $i < 3; ) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (; $i < 3; $i++) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (; ; ) {
        last if $i >= 3;
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for ($i = $i; $i < 3; $i += 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (my $k = 0; ; $k++) {
        last if $k > 4;
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (my $k = 0, my $m = 9; $k < $m; $k += 2, $m -= 3) {
        say(($k . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for ($i = 0, my $m = 3; $i < $m; $i++, $m--) {
        say(($i . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    say($i++) while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    $i++ while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    $i += 2 until $i >= 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    say($i--) while $i > 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    say(--$i) until $i <= 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    $i += $i while $i && ($i < 40);
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    while ($i < 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    until ($i >= 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    while (($i++) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    while ((++$i) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    until (($i++) > 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    while (($i += 2) < 7) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    while (!($i >= 3)) {
        say($i);
        $i++;
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for (my $k = 2; $k < 3; $k++) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for (my $k = 2; $k < 3; ++$k) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for (; $i < 3; ) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for (; $i < 3; $i++) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for (; ; ) {
        last if $i >= 3;
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for ($i = $i; $i < 3; $i += 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for (my $k = 2; ; $k++) {
        last if $k > 4;
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for (my $k = 2, my $m = 9; $k < $m; $k += 2, $m -= 3) {
        say(($k . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    for ($i = 2, my $m = 3; $i < $m; $i++, $m--) {
        say(($i . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    say($i++) while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    $i++ while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    $i += 2 until $i >= 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    say($i--) while $i > 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    say(--$i) until $i <= 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 2;
    $i += $i while $i && ($i < 40);
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    while ($i < 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    until ($i >= 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    while (($i++) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    while ((++$i) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    until (($i++) > 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    while (($i += 2) < 7) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    while (!($i >= 3)) {
        say($i);
        $i++;
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for (my $k = 3; $k < 3; $k++) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for (my $k = 3; $k < 3; ++$k) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for (; $i < 3; ) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for (; $i < 3; $i++) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for (; ; ) {
        last if $i >= 3;
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for ($i = $i; $i < 3; $i += 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for (my $k = 3; ; $k++) {
        last if $k > 4;
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for (my $k = 3, my $m = 9; $k < $m; $k += 2, $m -= 3) {
        say(($k . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    for ($i = 3, my $m = 3; $i < $m; $i++, $m--) {
        say(($i . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    say($i++) while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    $i++ while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    $i += 2 until $i >= 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    say($i--) while $i > 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    say(--$i) until $i <= 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    $i += $i while $i && ($i < 40);
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    while ($i < 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    until ($i >= 3) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    while (($i++) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    while ((++$i) < 3) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    until (($i++) > 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    while (($i += 2) < 7) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    while (!($i >= 3)) {
        say($i);
        $i++;
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for (my $k = 5; $k < 3; $k++) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for (my $k = 5; $k < 3; ++$k) {
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for (; $i < 3; ) {
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for (; $i < 3; $i++) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for (; ; ) {
        last if $i >= 3;
        say($i);
        $i++;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for ($i = $i; $i < 3; $i += 2) {
        say($i);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for (my $k = 5; ; $k++) {
        last if $k > 4;
        say($k);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for (my $k = 5, my $m = 9; $k < $m; $k += 2, $m -= 3) {
        say(($k . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    for ($i = 5, my $m = 3; $i < $m; $i++, $m--) {
        say(($i . ':') . $m);
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    say($i++) while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    $i++ while $i < 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    $i += 2 until $i >= 3;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    say($i--) while $i > 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    say(--$i) until $i <= 0;
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 5;
    $i += $i while $i && ($i < 40);
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    while ($i) {
        say($i);
        $i--;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 3;
    until (!$i) {
        say($i);
        $i--;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 1.5;
    while ($i) {
        say($i);
        $i -= 0.5;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $s = '3210';
    while ($s) {
        say($s);
        $s = substr($s, 1);
    }
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $s = 'abc';
    while ($s ne "") {
        say($s);
        $s = substr($s, 1);
    }
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $s = 'abc';
    until ($s eq "") {
        say($s);
        $s = substr($s, 0, length($s) - 1);
    }
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $s;
    while ($s) {
        say('not reached');
    }
    until (defined($s)) {
        $s = 'now';
    }
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $s = "";
    $s .= 'ab' while length($s) < 7;
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $s = 'x';
    $s x= 2 until length($s) > 20;
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $i = 1;
    while ($i < 1000) {
        $i *= 3;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 1;
    my $s = 0;
    while ($i <= 100) {
        $s += $i;
        $i++;
    }
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $i = 10;
    my $s = 1;
    for (; $i > 1; $i--) {
        $s *= $i;
    }
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
}
{
    my $i = 1.0;
    while ($i < 2) {
        say($i);
        $i += 0.25;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 27;
    my $k = 0;
    until ($i == 1) {
        $i = (($i % 2) ? (($i * 3) + 1) : ($i / 2));
        $k++;
    }
    say(defined($k) ? (('[' . $k) . ']') : 'undef');
}
{
    my $i = 0;
    while ($i < 3) {
        my $j = 0;
        while ($j < $i) {
            say(($i . '.') . $j);
            $j++;
        }
        say('end of ' . $i);
        $i++;
    }
}
{
    my $n = 0;
    my $i = 0;
    while ($i < 4) {
        my $j = 0;
        while ($j < 3) {
            $n++;
            $j++;
        }
        $i++;
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    while ($i < 3) {
        my $j = 0;
        until ($j >= $i) {
            say(($i . '.') . $j);
            $j++;
        }
        say('end of ' . $i);
        $i++;
    }
}
{
    my $n = 0;
    my $i = 0;
    while ($i < 4) {
        my $j = 0;
        until ($j >= 3) {
            $n++;
            $j++;
        }
        $i++;
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    while ($i < 3) {
        for (my $j = 0; $j < $i; $j++) {
            say(($i . '.') . $j);
        }
        say('end of ' . $i);
        $i++;
    }
}
{
    my $n = 0;
    my $i = 0;
    while ($i < 4) {
        for (my $j = 0; $j < 3; $j++) {
            $n++;
        }
        $i++;
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    until ($i >= 3) {
        my $j = 0;
        while ($j < $i) {
            say(($i . '.') . $j);
            $j++;
        }
        say('end of ' . $i);
        $i++;
    }
}
{
    my $n = 0;
    my $i = 0;
    until ($i >= 4) {
        my $j = 0;
        while ($j < 3) {
            $n++;
            $j++;
        }
        $i++;
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    until ($i >= 3) {
        my $j = 0;
        until ($j >= $i) {
            say(($i . '.') . $j);
            $j++;
        }
        say('end of ' . $i);
        $i++;
    }
}
{
    my $n = 0;
    my $i = 0;
    until ($i >= 4) {
        my $j = 0;
        until ($j >= 3) {
            $n++;
            $j++;
        }
        $i++;
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    until ($i >= 3) {
        for (my $j = 0; $j < $i; $j++) {
            say(($i . '.') . $j);
        }
        say('end of ' . $i);
        $i++;
    }
}
{
    my $n = 0;
    my $i = 0;
    until ($i >= 4) {
        for (my $j = 0; $j < 3; $j++) {
            $n++;
        }
        $i++;
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    for (my $i = 0; $i < 3; $i++) {
        my $j = 0;
        while ($j < $i) {
            say(($i . '.') . $j);
            $j++;
        }
        say('end of ' . $i);
    }
}
{
    my $n = 0;
    for (my $i = 0; $i < 4; $i++) {
        my $j = 0;
        while ($j < 3) {
            $n++;
            $j++;
        }
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    for (my $i = 0; $i < 3; $i++) {
        my $j = 0;
        until ($j >= $i) {
            say(($i . '.') . $j);
            $j++;
        }
        say('end of ' . $i);
    }
}
{
    my $n = 0;
    for (my $i = 0; $i < 4; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $n++;
            $j++;
        }
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    for (my $i = 0; $i < 3; $i++) {
        for (my $j = 0; $j < $i; $j++) {
            say(($i . '.') . $j);
        }
        say('end of ' . $i);
    }
}
{
    my $n = 0;
    for (my $i = 0; $i < 4; $i++) {
        for (my $j = 0; $j < 3; $j++) {
            $n++;
        }
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    if ($i == 0) {
        while ($i < 2) {
            say($i);
            $i++;
        }
    } else {
        say('not reached');
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while ($i < 6) {
        if (($i % 3) == 0) {
            say($i . ' fizz');
        } elsif (($i % 2) == 0) {
            say($i . ' even');
        } else {
            say($i);
        }
        $i++;
    }
}
{
    my $n = 0;
    for (my $i = 0; $i < 3; $i++) {
        for (my $j = 0; $j < 3; $j++) {
            for (my $k = 0; $k < 3; $k++) {
                $n += (($i + $j) + $k);
            }
        }
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    while ($i < 2) {
        $i++;
    }
    while ($i < 4) {
        say($i);
        $i++;
    }
    until ($i < 3) {
        $i--;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        say('odd') if $i % 2;
        say('even') unless $i % 2;
    }
}
{
    my $i = 0;
    while ($i < 3) {
        {
            $i++;
            say($i);
        }
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++ while $i < 2;
        say($i);
        $i++;
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
    }
}
{
    my $i = 0;
    for (; ($i++) < 3; ) {
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    for (my $k = 0, my $m = 0; $k < 3; $k++, $m = ($k * 10)) {
        say(($k . ':') . $m);
    }
}
{
    for (my $k = 0, my $m = 0; $k < 3; $m = ($k * 10), $k++) {
        say(($k . ':') . $m);
    }
}
{
    my $i = 0;
    my $j = 0;
    for ($i = 1, $j = ($i + 1); $i < 3; $j += $i, $i++) {
        say(($i . ':') . $j);
    }
}
