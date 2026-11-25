# What every test assumes of the runtime (D64, D65): a collection at every
# allocation, a collected string's memory never handed out again, and a
# cap of 256 MB on what a program may hold, so that one that runs away
# faults in a second. A test's own `# env:` header says otherwise for that
# test; a variable already set says otherwise for the run.
#
# t/run.sh sources this, and t/checks.py reads it: it is the one place the
# knobs are said, for every place a test's binary is run. One assignment
# to a line, in this shape.
: "${CURLY_GC_STRESS=1}"
: "${CURLY_GC_POISON=1}"
: "${CURLY_HEAP_CAP=268435456}"
export CURLY_GC_STRESS CURLY_GC_POISON CURLY_HEAP_CAP
