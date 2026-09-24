#include "hid_consumer_control.h"

#include <stdint.h>

// Consumer Control HID with two momentary buttons:
// bit 0: Volume Increment (Usage 0xE9)
// bit 1: Volume Decrement (Usage 0xEA)
static const uint8_t SC_HID_CONSUMER_CONTROL_REPORT_DESC[] = {
    0x05, 0x0C,       // Usage Page (Consumer)
    0x09, 0x01,       // Usage (Consumer Control)
    0xA1, 0x01,       // Collection (Application)
    0x15, 0x00,       // Logical Minimum (0)
    0x25, 0x01,       // Logical Maximum (1)
    0x09, 0xE9,       // Usage (Volume Increment)
    0x09, 0xEA,       // Usage (Volume Decrement)
    0x75, 0x01,       // Report Size (1)
    0x95, 0x02,       // Report Count (2)
    0x81, 0x02,       // Input (Data, Variable, Absolute)
    0x75, 0x06,       // Report Size (6)
    0x95, 0x01,       // Report Count (1)
    0x81, 0x01,       // Input (Constant)
    0xC0,             // End Collection
};

void
sc_hid_consumer_control_generate_open(struct sc_hid_open *hid_open) {
    hid_open->hid_id = SC_HID_ID_CONSUMER_CONTROL;
    hid_open->report_desc = SC_HID_CONSUMER_CONTROL_REPORT_DESC;
    hid_open->report_desc_size =
        sizeof(SC_HID_CONSUMER_CONTROL_REPORT_DESC);
}

void
sc_hid_consumer_control_generate_input(struct sc_hid_input *hid_input,
                                       bool volume_up, bool volume_down) {
    hid_input->hid_id = SC_HID_ID_CONSUMER_CONTROL;
    hid_input->size = 1;
    hid_input->data[0] = (volume_up ? 1 : 0) | (volume_down ? 2 : 0);
}
