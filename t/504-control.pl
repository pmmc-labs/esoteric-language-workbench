# model: t/models/var.py
use v5.42;
use open ':std', ':encoding(UTF-8)';
{
    my $v = 0;
    if (0) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif (0) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless (0) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif (1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless (1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ("") {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ("") {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ("") {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ("") {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ("") {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('0') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('0') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ('0') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('0') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ('0') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('0.0') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('0.0') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ('0.0') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('0.0') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ('0.0') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('a') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('a') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ('a') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ('a') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ('a') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0.0) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0.0) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif (0.0) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0.0) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless (0.0) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ((undef)) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ((undef)) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ((undef)) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ((undef)) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ((undef)) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (true) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (true) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif (true) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (true) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless (true) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (false) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (false) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif (false) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (false) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless (false) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v == 1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v == 1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ($v == 1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v == 1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ($v == 1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v < 2) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v < 2) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ($v < 2) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v < 2) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ($v < 2) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (!$v) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (!$v) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif (!$v) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (!$v) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless (!$v) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v += 1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v += 1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ($v += 1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v += 1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ($v += 1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v++) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v++) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ($v++) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v++) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ($v++) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v = ($v + 0)) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v = ($v + 0)) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ($v = ($v + 0)) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v = ($v + 0)) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ($v = ($v + 0)) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v && ($v = ($v + 6))) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v && ($v = ($v + 6))) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if (0) {
        say('first');
    } elsif ($v && ($v = ($v + 6))) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    if ($v && ($v = ($v + 6))) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    unless ($v && ($v = ($v + 6))) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') if $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    say('said') unless $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v = 50 if $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 0;
    $v++ unless $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif (0) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless (0) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif (1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless (1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ("") {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ("") {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ("") {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ("") {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ("") {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('0') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('0') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ('0') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('0') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ('0') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('0.0') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('0.0') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ('0.0') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('0.0') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ('0.0') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('a') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('a') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ('a') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ('a') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ('a') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0.0) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0.0) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif (0.0) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0.0) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless (0.0) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ((undef)) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ((undef)) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ((undef)) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ((undef)) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ((undef)) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (true) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (true) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif (true) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (true) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless (true) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (false) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (false) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif (false) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (false) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless (false) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v == 1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v == 1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ($v == 1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v == 1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ($v == 1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v < 2) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v < 2) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ($v < 2) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v < 2) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ($v < 2) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (!$v) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (!$v) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif (!$v) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (!$v) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless (!$v) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v += 1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v += 1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ($v += 1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v += 1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ($v += 1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v++) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v++) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ($v++) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v++) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ($v++) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v = ($v + 0)) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v = ($v + 0)) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ($v = ($v + 0)) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v = ($v + 0)) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ($v = ($v + 0)) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v && ($v = ($v + 6))) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v && ($v = ($v + 6))) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
        say('first');
    } elsif ($v && ($v = ($v + 6))) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v && ($v = ($v + 6))) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    unless ($v && ($v = ($v + 6))) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') if $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    say('said') unless $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v = 50 if $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    $v++ unless $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif (0) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless (0) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless 0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif (1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless (1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ("") {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ("") {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ("") {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ("") {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ("") {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless "";
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('0') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('0') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ('0') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('0') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ('0') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless '0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('0.0') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('0.0') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ('0.0') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('0.0') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ('0.0') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless '0.0';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('a') {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('a') {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ('a') {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ('a') {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ('a') {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless 'a';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0.0) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0.0) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif (0.0) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0.0) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless (0.0) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless 0.0;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ((undef)) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ((undef)) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ((undef)) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ((undef)) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ((undef)) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless (undef);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (true) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (true) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif (true) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (true) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless (true) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless true;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (false) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (false) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif (false) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (false) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless (false) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless false;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v == 1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v == 1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ($v == 1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v == 1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ($v == 1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless $v == 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v < 2) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v < 2) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ($v < 2) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v < 2) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ($v < 2) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless $v < 2;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (!$v) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (!$v) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif (!$v) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (!$v) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless (!$v) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless !$v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v += 1) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v += 1) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ($v += 1) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v += 1) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ($v += 1) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless $v += 1;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v++) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v++) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ($v++) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v++) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ($v++) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless $v++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v = ($v + 0)) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v = ($v + 0)) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ($v = ($v + 0)) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v = ($v + 0)) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ($v = ($v + 0)) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless $v = ($v + 0);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v && ($v = ($v + 6))) {
        say('then');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v && ($v = ($v + 6))) {
        say('then');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if (0) {
        say('first');
    } elsif ($v && ($v = ($v + 6))) {
        say('second');
    } else {
        say('else');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    if ($v && ($v = ($v + 6))) {
        say('first');
    } elsif (1) {
        say('second');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    unless ($v && ($v = ($v + 6))) {
        say('unless');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') if $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    say('said') unless $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v = 50 if $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 2;
    $v++ unless $v && ($v = ($v + 6));
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    {
        my $v = 2;
        say(defined($v) ? (('[' . $v) . ']') : 'undef');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    {
        my $v = $v + 10;
        say(defined($v) ? (('[' . $v) . ']') : 'undef');
        $v++;
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    {
        $v = 2;
        my $v = 3;
        $v = 4;
        say(defined($v) ? (('[' . $v) . ']') : 'undef');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if ($v) {
        my $v = 'inner';
        say(defined($v) ? (('[' . $v) . ']') : 'undef');
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    if (0) {
    } elsif (1) {
        my $w = $v + 1;
        $v = $w;
    } else {
        my $v = 9;
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    $v = 'set';
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    my $w = $v;
    $w++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 1;
    my $w = $v = 5;
    $w++;
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 1;
    {
        {
            $v += 1;
        }
    }
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
}
{
    my $v = 1;
    my $w = 2;
    $v = ($w = 7);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
{
    my $v = 1;
    my $w = 2;
    $v += ($w *= 7);
    say(defined($v) ? (('[' . $v) . ']') : 'undef');
    say(defined($w) ? (('[' . $w) . ']') : 'undef');
}
