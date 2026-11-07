# Every target runs from the repository root. See CLAUDE.md "Commands".
SANITIZE := -fsanitize=undefined,address -fno-sanitize-recover=all -g
WARN := -Wall -Wextra -Werror

.PHONY: test unit golden golden-clang sanitize checks

test: unit golden golden-clang sanitize checks

unit:
	node --test 'compiler/tests/*.test.ts'

golden:
	T_TAG=cc LANG_CFLAGS="$(WARN)" t/run.sh

golden-clang:
	T_TAG=clang LANG_CC=clang LANG_CFLAGS="$(WARN)" t/run.sh

sanitize:
	T_TAG=san LANG_CC=clang LANG_CFLAGS="$(SANITIZE)" t/run.sh

checks:
	python3 t/checks.py
