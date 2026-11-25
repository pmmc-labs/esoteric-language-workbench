# model: t/models/loop.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    while ($i < 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: while ($i < 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    until ($i >= 3) {
        $i++;
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $i = 0;
    OUTER: until ($i >= 3) {
        $i++;
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        while ($j < 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        INNER: until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        my $j = 0;
        until ($j >= 3) {
            $j++;
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last INNER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                last INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    last INNER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        last INNER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            last OUTER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                last OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                last OUTER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next INNER unless $j != 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j != 2) {
                say('stay');
            } else {
                next INNER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    for (my $i = 1; $i <= 3; $i++) {
        INNER: for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                next INNER if $j == 2;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            next OUTER if $j == 2;
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j == 2) {
                say('jump');
                next OUTER;
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            if ($j < 2) {
                say('low');
            } elsif ($j == 2) {
                if ($i) {
                    next OUTER;
                }
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    OUTER: for (my $i = 1; $i <= 3; $i++) {
        for (my $j = 1; $j <= 3; $j++) {
            say(('a' . $i) . $j);
            {
                {
                    if ($j == 2) {
                        next OUTER;
                    }
                }
                say('in the block');
            }
            say(('b' . $i) . $j);
        }
        say('c' . $i);
    }
    say('d');
}
{
    my $k = 0;
    for ($k = 0; $k < 5; $k++) {
        last if $k == 2;
    }
    say(defined($k) ? (('[' . $k) . ']') : 'undef');
}
{
    my $k = 0;
    my $n = 0;
    for ($k = 0; $k < 5; $k++) {
        next if $k == 2;
        $n++;
    }
    say(defined($k) ? (('[' . $k) . ']') : 'undef');
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $k = 0;
    my $n = 0;
    for (; $k < 5; $k++, $n++) {
        next;
    }
    say(defined($k) ? (('[' . $k) . ']') : 'undef');
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    while (1) {
        last;
    }
    say('after');
}
{
    my $i = 0;
    while (($i++) < 3) {
        next;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    while (1) {
        $i++;
        say($i);
        last;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    until (0) {
        $i++;
        next if $i < 3;
        last;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    for (; ; ) {
        $i++;
        next unless $i > 4;
        last;
    }
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
{
    my $i = 0;
    L: while (($i++) < 3) {
        my $j = 0;
        L: while (1) {
            $j++;
            last L if $j == 2;
        }
        say($i . $j);
    }
}
{
    my $i = 0;
    L: while (($i++) < 3) {
        my $j = 0;
        L: while (($j++) < 3) {
            next L if $j == 2;
            say($i . $j);
        }
    }
}
{
    my $n = 0;
    A: for (my $i = 0; $i < 3; $i++) {
        B: for (my $j = 0; $j < 3; $j++) {
            C: for (my $k = 0; $k < 3; $k++) {
                $n++;
                last A if $n == 14;
            }
        }
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $n = 0;
    A: for (my $i = 0; $i < 3; $i++) {
        B: for (my $j = 0; $j < 3; $j++) {
            C: for (my $k = 0; $k < 3; $k++) {
                next B if $k == 1;
                $n++;
            }
        }
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $n = 0;
    A: for (my $i = 0; $i < 3; $i++) {
        B: for (my $j = 0; $j < 3; $j++) {
            C: for (my $k = 0; $k < 3; $k++) {
                next A if $j == 1;
                last B if $i == 2;
                next C unless $k;
                $n++;
            }
        }
    }
    say(defined($n) ? (('[' . $n) . ']') : 'undef');
}
{
    my $i = 0;
    while ((my $d = ($i++)) < 5) {
        next if $d % 2;
        say($d);
    }
}
{
    my $i = 0;
    ONLY: while (($i++) < 5) {
        next ONLY if $i == 2;
        last ONLY if $i == 4;
        say($i);
    }
}
{
    my $i = 0;
    UNUSED_1: until (($i++) >= 2) {
        say($i);
    }
}
{
    my $i = 0;
    my $s = "";
    while (1) {
        $s .= $i;
        last if ($i++) >= 3;
        $s .= '-';
    }
    say(defined($s) ? (('[' . $s) . ']') : 'undef');
    say(defined($i) ? (('[' . $i) . ']') : 'undef');
}
