use v5.42;
print __FILE__ =~ /yq\d+\.pl$/ ? "file" : "other", __LINE__, "\n";
