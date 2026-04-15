#ifndef WIFI_NETWORK_H
#define WIFI_NETWORK_H

#define MAX_SSID_LEN 32

typedef enum {
    SEC_OPEN = 0,
    SEC_WEP,
    SEC_WPA,
    SEC_WPA2,
    SEC_WPA3
} security_t;

typedef struct {
    char ssid[MAX_SSID_LEN + 1];
    char bssid[18];          // "aa:bb:cc:dd:ee:ff"
    char vendor[128];        // Cisco Systems, Inc
    int rssi;                // dBm
    int channel;             // 1-13
    int frequency;           // MHz
    security_t security;
    uint8_t bandwidth;
} wifi_network_t;

typedef struct{
    char prefix[7];
    char vendor[128];
} vendor_entry_t;

typedef struct {
    int8_t rssi;
    uint16_t frequency;
} radiotap_data_t;

#endif

