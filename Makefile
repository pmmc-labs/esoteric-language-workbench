SAN = -fsanitize=undefined,address -fno-sanitize-recover=all -g
TESTS = $(sort $(wildcard t/*.strata examples/*.strata))

.PHONY: test unit golden golden-clang sanitize checks tools

test: unit golden golden-clang sanitize checks

unit:
	node --test compiler/tests/*.test.ts

# Runs every golden test, reports all failures, then fails if any did.
golden:
	@fail=0; n=0; for f in $(TESTS); do n=$$((n+1)); t/run.sh $$f || fail=$$((fail+1)); done; \
	echo "golden ($${LANG_CC:-cc}): $$((n-fail))/$$n passed"; [ $$fail -eq 0 ]

golden-clang:
	@$(MAKE) --no-print-directory golden LANG_CC=clang

sanitize:
	@$(MAKE) --no-print-directory golden LANG_CC=clang LANG_CFLAGS="$(SAN)"

checks:
	python3 t/checks.py

tools:
	@node --version; cc --version | head -1; clang --version | head -1
