use v5.42;
print scalar reverse("abc"), " ", join("", reverse("ab","cd")), " ", scalar reverse("ab","cd"), "\n";
