# make test     the compiler's unit tests, then the golden tests (t/run.sh)
# make unit     the unit tests alone (node:test)
# make golden   the golden tests alone; JOBS=n runs n at once
# make check    type-check the compiler (needs `npm install` first)
# make clean    remove build/
#
# Step 0 compiles to C and links with cc, so a binary runs on the machine
# that built it and nothing is cross-compiled. When a native target comes,
# TARGETS and a cross-compiler plus emulator go here, as a64-slight's
# Makefile has them.

test: unit golden

unit:
	node --test "compiler/tests/**/*.test.ts"

golden:
	@./t/run.sh

check:
	npx tsc --noEmit

clean:
	rm -rf build

.PHONY: test unit golden check clean
