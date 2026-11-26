use v5.42;
package P; sub who { __PACKAGE__ } package Q; sub who { __PACKAGE__ . P::who() } package main; print Q::who(), __PACKAGE__, "\n";
