#include "ditto.h"

int main(void) {
  dt_path = "b1.ditto";
  Value t1 = dt_int(INT64_C(1));
  Value v_x = t1;
  (void)v_x;
  {
    Value t2 = v_x;
    Value a3[] = {t2};
    Value t3 = dt_b_print(2, 1, 1, a3);
    (void)t3;
  }
  return 0;
}
