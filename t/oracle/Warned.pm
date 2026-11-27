# For t/checks.py alone, never for a test. The oracle's look at a test's
# stderr (step 15; D149): perl is run once more with this loaded, and
# every warning that does not come from the program's own `warn` is
# marked, so that a `dies` or a `warns` test in which perl itself warned
# fails the check. `warn` is overridden to say which warnings are the
# program's; an undef among its arguments is perl's own warning too
# (`Use of uninitialized value in warn`).
package Warned;
our $own = 0;
BEGIN {
    *CORE::GLOBAL::warn = sub {
        print STDERR "PERL WARNED: an undef in a warn's list\n" if grep { !defined } @_;
        local $own = 1;
        CORE::warn(@_);
    };
    $SIG{__WARN__} = sub { print STDERR ($own ? '' : 'PERL WARNED: '), $_[0] };
}
1;
