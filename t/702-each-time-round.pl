# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
        $x = $i;
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
        $x = $i;
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
        $x = $i;
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        $x .= 'a';
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        $x .= 'a';
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        $x .= 'a';
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        $x++;
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        $x++;
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        $x++;
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        $x += $i;
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        $x += $i;
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        $x += $i;
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        $x //= $i;
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        $x //= $i;
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        $x //= $i;
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        $x ||= $i;
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        $x ||= $i;
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        $x ||= $i;
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        if ($i == 1) {
            $x = 'one';
        } elsif ($i == 2) {
            $x = 2.5;
        }
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        if ($i == 1) {
            $x = 'one';
        } elsif ($i == 2) {
            $x = 2.5;
        }
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        if ($i == 1) {
            $x = 'one';
        } elsif ($i == 2) {
            $x = 2.5;
        }
        say(defined($x) ? (('[' . $x) . ']') : 'undef');
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        next if $i == 2;
        my $x;
        $x .= 'a';
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        next if $i == 2;
        my $x;
        $x .= 'a';
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        next if $i == 2;
        my $x;
        $x .= 'a';
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        $x .= 'a';
        next if $i == 2;
        $x .= 'b';
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        $x .= 'a';
        next if $i == 2;
        $x .= 'b';
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        $x .= 'a';
        next if $i == 2;
        $x .= 'b';
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        if ($i != 2) {
            my $x;
            $x .= $i;
            say($x);
        } else {
            my $x;
            $x--;
            say($x);
        }
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        if ($i != 2) {
            my $x;
            $x .= $i;
            say($x);
        } else {
            my $x;
            $x--;
            say($x);
        }
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        if ($i != 2) {
            my $x;
            $x .= $i;
            say($x);
        } else {
            my $x;
            $x--;
            say($x);
        }
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        {
            my $x;
            $x .= $i;
            say($x);
        }
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        {
            my $x;
            $x .= $i;
            say($x);
        }
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        {
            my $x;
            $x .= $i;
            say($x);
        }
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x = $i;
        {
            my $x;
            say(defined($x) ? (('[' . $x) . ']') : 'undef');
            $x = 'inner';
        }
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x = $i;
        {
            my $x;
            say(defined($x) ? (('[' . $x) . ']') : 'undef');
            $x = 'inner';
        }
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x = $i;
        {
            my $x;
            say(defined($x) ? (('[' . $x) . ']') : 'undef');
            $x = 'inner';
        }
        say($x);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x = $i * 10;
        say($x);
        $x++;
        my $y = $x;
        say($y);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x = $i * 10;
        say($x);
        $x++;
        my $y = $x;
        say($y);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x = $i * 10;
        say($x);
        $x++;
        my $y = $x;
        say($y);
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $j = 0;
        while (($j++) < 2) {
            my $x;
            $x .= ($i . $j);
            say($x);
        }
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        while (($j++) < 2) {
            my $x;
            $x .= ($i . $j);
            say($x);
        }
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while (($j++) < 2) {
            my $x;
            $x .= ($i . $j);
            say($x);
        }
    }
}
{
    my $i = 0;
    while (($i++) < 3) {
        my $x;
        for (my $j = 0; $j < 2; $j++) {
            $x .= $j;
        }
        say($x);
    }
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $x;
        for (my $j = 0; $j < 2; $j++) {
            $x .= $j;
        }
        say($x);
    }
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $x;
        for (my $j = 0; $j < 2; $j++) {
            $x .= $j;
        }
        say($x);
    }
}
{
    my $x;
    my $i = 0;
    while (($i++) < 3) {
        $x .= $i;
        say($x);
    }
}
{
    my $x;
    my $i = 0;
    until ($i >= 3) {
        $i++;
        $x .= $i;
        say($x);
    }
}
{
    my $x;
    for (my $i = 1; $i <= 3; $i++) {
        $x .= $i;
        say($x);
    }
}
{
    my $x = 10;
    my $i = 0;
    while (($i++) < 3) {
        $x++;
        my $x = 'hidden';
        $x .= '!';
    }
}
{
    my $x = 10;
    my $i = 0;
    until ($i >= 3) {
        $i++;
        $x++;
        my $x = 'hidden';
        $x .= '!';
    }
}
{
    my $x = 10;
    for (my $i = 1; $i <= 3; $i++) {
        $x++;
        my $x = 'hidden';
        $x .= '!';
    }
}
{
    my $i = 0;
    while ((my $x .= 'a') && (($i++) < 3)) {
        say($x);
        $x .= 'b';
        say($x);
    }
}
{
    my $i = 0;
    until ((my $x = ($i++)) > 2) {
        say($x);
        $x += 10;
    }
}
{
    my $i = 0;
    while ((my $x += ($i++)) < 3) {
        say($x);
    }
}
{
    my $i = 0;
    while ((my $x //= ($i++)) < 3) {
        say($x);
        $x = 99;
    }
}
{
    my $i = 3;
    while (my $x = ($i--)) {
        say($x);
    }
}
{
    my $i = 0;
    while ((my $x = ($i++)) < 3) {
        my $x = 's';
        say($x);
    }
}
{
    my $x = 'outer';
    my $i = 0;
    while ((my $x = ($i++)) < 2) {
        say($x);
    }
    say($x);
}
{
    my $i = 0;
    while ((my $x = ($i++)) < 3) {
        my $j = 0;
        while ((my $y = ($j++)) < 2) {
            say($x . $y);
        }
    }
}
{
    for (my $k = 0, my $x = ""; $k < 3; $k++) {
        $x .= $k;
        say($x);
    }
}
{
    for (my $k = 0; $k < 3; $k++) {
        my $k = 9;
        say($k);
    }
}
{
    for (my $k = 0; $k < 6; $k++) {
        $k++;
        say($k);
    }
}
{
    my $k = 'outer';
    for (my $k = 0; $k < 2; $k++) {
        say($k);
    }
    say($k);
}
{
    my $k = 5;
    for (my $k = ($k + 1); $k < 8; $k++) {
        say($k);
    }
    say($k);
}
{
    for (my $k = 0; $k < 2; $k++) {
        for (my $k = 5; $k < 7; $k++) {
            say($k);
        }
        say($k);
    }
}
