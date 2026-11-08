#include "ditto.h"

int main(void) {
  dt_path = "b4.ditto";
  {
    Value t1 = dt_int(INT64_C(1));
    Value a2[] = {t1};
    Value t2 = dt_b_print(1, 1, 1, a2);
    (void)t2;
  }
  {
    Value t3 = dt_int(INT64_C(2));
    Value a4[] = {t3};
    Value t4 = dt_b_print(2, 1, 1, a4);
    (void)t4;
  }
  return 0;
}
