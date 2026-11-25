use v5.42;
# `&&=` on an element past the end stores nothing and makes the array longer.
my @a;
$a[5] &&= 1;
say scalar(@a);
