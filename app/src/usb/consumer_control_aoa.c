#include "consumer_control_aoa.h"

#include "hid/hid_consumer_control.h"
#include "util/log.h"

bool
sc_consumer_control_aoa_init(struct sc_consumer_control_aoa *cc,
                             struct sc_aoa *aoa) {
    cc->aoa = aoa;

    struct sc_hid_open hid_open;
    sc_hid_consumer_control_generate_open(&hid_open);

    if (!sc_aoa_push_open(aoa, &hid_open, false)) {
        LOGW("Could not push AOA HID open (consumer control)");
        return false;
    }

    return true;
}

bool
sc_consumer_control_aoa_set_volume(struct sc_consumer_control_aoa *cc,
                                   bool volume_up, bool volume_down) {
    struct sc_hid_input input;
    sc_hid_consumer_control_generate_input(&input, volume_up, volume_down);

    if (!sc_aoa_push_input(cc->aoa, &input)) {
        LOGW("Could not push AOA HID input (consumer control)");
        return false;
    }

    return true;
}

void
sc_consumer_control_aoa_destroy(struct sc_consumer_control_aoa *cc) {
    (void) cc;
    // sc_aoa_destroy() unregisters all AOA HID devices.
}
