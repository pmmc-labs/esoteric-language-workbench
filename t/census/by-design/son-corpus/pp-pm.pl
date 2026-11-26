use v5.42;
package O { sub m { $_[1] * 2 } } print O->m(5) + O->m(6), "\n";
