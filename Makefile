# make test     the compiler's unit tests, the golden tests (t/run.sh), and
#               the mechanical checks (t/checks.py: every model's files are
#               what it writes now; every test has its .expected)
# make unit     the unit tests alone (node:test)
# make golden   the golden tests alone; JOBS=n runs n at once
# make checks   the mechanical checks alone
# make models   rerun every model and write its files (never patch them)
# make commits  every commit since origin/main that touches the
#               implementation names a decision or a plan step
# make hooks    install the commit-msg hook that checks that as you commit
# make check    type-check the compiler (needs `npm install` first)
# make clean    remove build/
#
# Step 0 compiles to C and links with cc, so a binary runs on the machine
# that built it and nothing is cross-compiled. When a native target comes,
# TARGETS and a cross-compiler plus emulator go here, as a64-slight's
# Makefile has them.

test: unit golden checks

unit:
	node --test "compiler/tests/**/*.test.ts"

golden:
	@./t/run.sh

checks:
	@python3 t/checks.py

models:
	@python3 t/checks.py models --write

commits:
	@python3 t/checks.py commits

hooks:
	@printf '#!/bin/sh\nexec python3 t/checks.py commit-msg "$$1" --staged\n' > .git/hooks/commit-msg
	@chmod +x .git/hooks/commit-msg
	@echo "installed .git/hooks/commit-msg"

check:
	npx tsc --noEmit

clean:
	rm -rf build

.PHONY: test unit golden checks models commits hooks check clean
