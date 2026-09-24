#ifndef SC_CONSUMER_CONTROL_AOA_H
#define SC_CONSUMER_CONTROL_AOA_H

#include "common.h"

#include <stdbool.h>

#include "usb/aoa_hid.h"

struct sc_consumer_control_aoa {
    struct sc_aoa *aoa;
};

bool
sc_consumer_control_aoa_init(struct sc_consumer_control_aoa *cc,
                             struct sc_aoa *aoa);

bool
sc_consumer_control_aoa_set_volume(struct sc_consumer_control_aoa *cc,
                                   bool volume_up, bool volume_down);

void
sc_consumer_control_aoa_destroy(struct sc_consumer_control_aoa *cc);

#endif
