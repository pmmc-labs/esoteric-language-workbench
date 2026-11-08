#include "ditto.h"

int main(void) {
  dt_path = "b2.ditto";
  {
    Value t1 = dt_int(INT64_C(1));
    Value a2[] = {t1};
    Value t2 = dt_b_print(2, 1, 1, a2);
    (void)t2;
  }
  return 0;
}
