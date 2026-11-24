import { test } from 'node:test';
import assert from 'node:assert/strict';
import { cString } from '../src/codegen.ts';

// What the generated C does is the golden tests' to say, by running it.
// This is the one piece they can't reach: no test's path has a quote in it.
test('a C string literal of any path', () => {
    assert.equal(cString('t/000-say.pl'), '"t/000-say.pl"');
    assert.equal(cString('a "b"\\c.pl'), '"a \\042b\\042\\134c.pl"');
    assert.equal(cString('what??/.pl'), '"what\\077\\077/.pl"');
    assert.equal(cString('café\n1.pl'), '"caf\\303\\251\\0121.pl"');
});
