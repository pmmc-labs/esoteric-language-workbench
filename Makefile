# make test     the unit tests, the golden tests (t/run.sh), and the mechanical
#               checks (t/checks.py: every model's files are what it writes now;
#               every test has its .expected; every referee in t/referee/ agrees
#               with every test it covers)
# make unit     the unit tests alone (node:test)
# make golden   the golden tests alone; JOBS=n runs n at once
# make checks   the mechanical checks alone
# make models   rerun every model and write its files (never patch them)
# make commits  every commit since origin/main that touches the implementation
#               names a decision or a plan step
# make hooks    install the commit-msg hook that checks that as you commit
# make check    type-check the interpreter (needs `npm install` first)
# make clean    remove build/

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

# The hooks directory asked of git, since in a worktree .git is a file
# and the hooks are the main checkout's.
hooks:
	@dir=$$(git rev-parse --git-path hooks) && mkdir -p "$$dir" && \
	printf '#!/bin/sh\nexec python3 t/checks.py commit-msg "$$1" --staged\n' > "$$dir/commit-msg" && \
	chmod +x "$$dir/commit-msg" && echo "installed $$dir/commit-msg"

check:
	npx tsc --noEmit

clean:
	rm -rf build

.PHONY: test unit golden checks models commits hooks check clean
