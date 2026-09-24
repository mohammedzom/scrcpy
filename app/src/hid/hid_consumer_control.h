#ifndef SC_HID_CONSUMER_CONTROL_H
#define SC_HID_CONSUMER_CONTROL_H

#include "common.h"

#include <stdbool.h>

#include "hid/hid_event.h"

#define SC_HID_ID_CONSUMER_CONTROL 4

void
sc_hid_consumer_control_generate_open(struct sc_hid_open *hid_open);

void
sc_hid_consumer_control_generate_input(struct sc_hid_input *hid_input,
                                       bool volume_up, bool volume_down);

#endif
