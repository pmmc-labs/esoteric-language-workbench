use v5.42;
package Greet;
sub hello { return "hello" }
package main;
sub shout { return "HELLO" }
print ::shout(), "\n";
print ::Greet::hello(), "\n";
