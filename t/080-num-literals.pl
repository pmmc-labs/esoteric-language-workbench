# Every way to write a number (D38), and numbers hard against operators.
use v5.42;
say 1.5; say .5; say 0.25; say 10.0; say 1e3; say 1E3; say 1.5e-3; say .5E+2;
say 0e0; say 1e007; say 1e-01; say 0.0; say .0; say 0.000;
say 0x1F; say 0X1f; say 0xff; say 0xAbCd; say 0xFFFFFFFF; say 0x0;
say 0b101; say 0B101; say 0b11111111111111111111111111111111; say 0b0;
say 0o17; say 0O17; say 0o37777777777; say 0o0;
say 1_000; say 1_0_0; say 1.5_0; say 1_0.2_5; say 1e1_0; say 0xff_ff; say 0b1_0; say 0o1_7; say .5_5;
say 2*.5; say 2**.5; say 7%1.5; say 1e3-1; say 1e-3-1; say 1e+3+1; say 1/.5; say 2**-.5;
say -.5; say +.5; say - .5; say(.5); say (.5); say -1.5e3; say -0x10; say -0b11; say -0o17;
say 1.7976931348623157e308; say 5e-324; say 1e-400; say 0.1; say 123456789012345678901234567890.0;
say 0x1F + 0b11 + 0o17; say 1e15 + 0; say 9007199254740993.0;
