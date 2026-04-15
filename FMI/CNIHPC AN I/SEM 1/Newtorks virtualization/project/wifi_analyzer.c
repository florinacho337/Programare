#include <pcap.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>

#include "wifi_network.h"

#define IFACE "wlp2s0"
#define HOP_INTERVAL 2   // seconds

/* ================= IEEE 802.11 ================= */

struct ieee80211_hdr {
    uint16_t frame_control;
    uint16_t duration;
    uint8_t  addr1[6];
    uint8_t  addr2[6];   // BSSID
    uint8_t  addr3[6];
    uint16_t seq_ctrl;
};

/* =================== VENDOR =================== */

vendor_entry_t vendors[60000];
int vendor_count = 0;

/* ================= Utilitare ================= */

void mac_to_str(const uint8_t *mac, char *buf) {
    sprintf(buf, "%02x:%02x:%02x:%02x:%02x:%02x",
            mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
}

void normalize_mac(const char* mac_in, char* mac_out) {
    int j = 0;
    for (int i = 0; mac_in[i] && j < 12; i++) {
        if (isxdigit(mac_in[i])) {
            mac_out[j++] = tolower(mac_in[i]);
        }
    }
    mac_out[j] = '\0';
}

const char* sec_to_str(security_t s) {
    switch (s) {
        case SEC_OPEN: return "OPEN";
        case SEC_WEP:  return "WEP";
        case SEC_WPA:  return "WPA";
        case SEC_WPA2: return "WPA2";
        case SEC_WPA3: return "WPA3";
        default:       return "UNKNOWN";
    }
}

void load_vendors(const char* filename) {
    FILE *f = fopen(filename, "r");
    if (!f) { perror("Cannot open vendors file"); exit(1); }

    char line[512];
    fgets(line, sizeof(line), f);

    while (fgets(line, sizeof(line), f)) {
        if (vendor_count >= 60000) break;

        char *mac_prefix = strtok(line, ",");
        char *vendor_name = strtok(NULL, ",");

        if (mac_prefix && vendor_name) {
            char clean_prefix[13];
            normalize_mac(mac_prefix, clean_prefix);

            strncpy(vendors[vendor_count].prefix, clean_prefix, 6);
            vendors[vendor_count].prefix[6] = '\0';

            if (vendor_name[0] == '"') {
                memmove(vendor_name, vendor_name+1, strlen(vendor_name));
                char *end = strchr(vendor_name, '"');
                if (end) *end = '\0';
            }

            strncpy(vendors[vendor_count].vendor, vendor_name, 127);
            vendors[vendor_count].vendor[127] = '\0';

            vendor_count++;
        }
    }
    fclose(f);
}

const char* get_vendor(const char* mac) {
    char clean_mac[13];
    normalize_mac(mac, clean_mac);

    for (int i = 0; i < vendor_count; i++) {
        if (strncmp(clean_mac, vendors[i].prefix, 6) == 0) {
            return vendors[i].vendor;
        }
    }
    return "UNKNOWN";
}

void parse_radiotap(const u_char *packet, uint16_t rt_len, radiotap_data_t *data)
{
    const uint8_t *ptr = packet;

    // === Citește toate it_present ===
    const uint32_t *present_ptr = (const uint32_t *)(packet + 4);
    uint32_t present[8];
    int npresent = 0;

    do {parse_radiotap
        present[npresent] = *present_ptr++;
    } while (present[npresent++] & 0x80000000);

    // ptr ajunge la începutul câmpurilor
    ptr = (const uint8_t *)present_ptr;
    const uint8_t *end = packet + rt_len;

    int bit_index = 0;

    // === Parcurge câmpurile ===
    for (int i = 0; i < npresent; i++) {
        uint32_t p = present[i];

        for (int bit = 0; bit < 32; bit++, bit_index++) {

            if (!(p & (1U << bit)))
                continue;

            int size = 0;

            switch (bit_index) {
                case 0:  size = 8; break; // TSFT
                case 1:  size = 1; break; // Flags
                case 2:  size = 1; break; // Rate
                case 3:  size = 4; break; // Channel
                case 4:  size = 2; break; // FHSS
                case 5:  size = 1; break; // dBm Ant Signal
                default:
                    size = 0;
                    break;
            }

            if (ptr + size > end)
                return;

	    if (bit_index == 3)
	        data->frequency = *(const uint16_t *)ptr;
            else if (bit_index == 5)
                data->rssi = *(const int8_t *)ptr;

            ptr += size;
        }
    }
}

/* ================= Channel Hopper Thread ================= */

void* channel_hopper(void* arg) {
    int channels[] = {1,2,3,4,5,6,7,8,9,10,11,12,13};
    int count = sizeof(channels)/sizeof(int);
    int i = 0;
    char cmd[128];

    while (1) {
        sprintf(cmd, "iw dev %s set channel %d", IFACE, channels[i]);
        system(cmd);

        i = (i + 1) % count;
        sleep(HOP_INTERVAL);
    }
    return NULL;
}

/* ================= Packet Handler ================= */

void handle_packet(u_char *args,
                   const struct pcap_pkthdr *header,
                   const u_char *packet) {

    wifi_network_t net;
    memset(&net, 0, sizeof(net));

    net.security = SEC_OPEN;
    net.bandwidth = 20;

    bool has_privacy = false;
    bool has_wpa_ie = false;
    bool has_rsn_ie = false;
    bool has_wpa3 = false;

    // ================= Radiotap =================
    uint16_t rt_len = *(uint16_t *)(packet + 2);
    radiotap_data_t rt_data = {0, 0};

    parse_radiotap(packet, rt_len, &rt_data);
    net.rssi = rt_data.rssi;
    net.frequency = rt_data.frequency;

    // ================= 802.11 Header =================
    const u_char *ptr = packet + rt_len;
    struct ieee80211_hdr *hdr = (struct ieee80211_hdr *)ptr;

    uint16_t fc = hdr->frame_control;
    int type = (fc >> 2) & 0x3;
    int subtype = (fc >> 4) & 0xF;

    // Doar Beacon Frames
    if (!(type == 0 && subtype == 8))
        return;

    // Privacy bit (WEP / WPA / WPA2 / WPA3)
    has_privacy = fc & (1 << 14);

    mac_to_str(hdr->addr2, net.bssid);
    const char *vendor = get_vendor(net.bssid);
    strncpy(net.vendor, vendor, sizeof(net.vendor) - 1);
    net.vendor[sizeof(net.vendor) - 1] = '\0';

    // ================= Beacon fixed params =================
    ptr += sizeof(struct ieee80211_hdr);
    ptr += 12;

    const u_char *end = packet + header->caplen;

    // ================= IE Parsing =================
    while (ptr + 2 < end) {
        uint8_t id = ptr[0];
        uint8_t len = ptr[1];
        const u_char *data = ptr + 2;

        if (ptr + 2 + len > end)
            break;

        switch (id) {

            // -------- SSID --------
            case 0:
                if (len > 0 && len < sizeof(net.ssid)) {
                    memcpy(net.ssid, data, len);
                    net.ssid[len] = '\0';
                }
                break;

            // -------- Channel --------
            case 3:
                net.channel = data[0];
                break;

            // -------- RSN (WPA2 / WPA3) --------
            case 48: {
                has_rsn_ie = true;

                if (len >= 10) {
                    uint16_t pairwise_count = data[6] | (data[7] << 8);
                    uint16_t akm_offset = 8 + pairwise_count * 4;

                    if (akm_offset + 2 <= len) {
                        uint16_t akm_count =
                            data[akm_offset] | (data[akm_offset + 1] << 8);

                        const uint8_t *akm_list = data + akm_offset + 2;

                        for (int i = 0; i < akm_count; i++) {
                            const uint8_t *akm = akm_list + i * 4;

                            // OUI 00:0f:ac
                            if (akm[0] == 0x00 &&
                                akm[1] == 0x0f &&
                                akm[2] == 0xac &&
                                akm[3] == 0x08) {
                                has_wpa3 = true; // SAE
                            }
                        }
                    }
                }
                break;
            }

            // -------- WPA (Vendor IE) --------
            case 221:
                if (len >= 4 &&
                    data[0] == 0x00 &&
                    data[1] == 0x50 &&
                    data[2] == 0xF2 &&
                    data[3] == 0x01) {
                    has_wpa_ie = true;
                }
                break;

            // -------- HT (802.11n) --------
            case 61:
                if (len >= 2 && (data[1] & 0x03) == 0x01)
                    net.bandwidth = 40;
                break;

            // -------- VHT (802.11ac) --------
            case 192:
                if (len >= 1) {
                    if (data[0] == 1) net.bandwidth = 80;
                    else if (data[0] == 2) net.bandwidth = 160;
                }
                break;
        }

        ptr += 2 + len;
    }

    // ================= FINAL SECURITY DECISION =================
    if (has_wpa3)
        net.security = SEC_WPA3;
    else if (has_rsn_ie)
        net.security = SEC_WPA2;
    else if (has_wpa_ie)
        net.security = SEC_WPA;
    else if (has_privacy)
        net.security = SEC_WEP;
    else
        net.security = SEC_OPEN;

    // ================= OUTPUT =================
    printf(
        "{\"type\":\"network\","
        "\"ssid\":\"%s\","
        "\"bssid\":\"%s\","
        "\"vendor\":\"%s\","
        "\"rssi\":%d,"
        "\"channel\":%d,"
        "\"freq\":%d,"
        "\"security\":\"%s\","
        "\"bandwidth\":%d}\n",
        net.ssid,
        net.bssid,
        net.vendor,
        net.rssi,
        net.channel,
        net.frequency,
        sec_to_str(net.security),
        net.bandwidth
    );

    fflush(stdout);
}

/* ================= Main ================= */

int main() {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;

    pthread_t hopper_thread;
    pthread_create(&hopper_thread, NULL, channel_hopper, NULL);

    handle = pcap_open_live(IFACE, BUFSIZ, 1, 1000, errbuf);
    if (!handle) {
        fprintf(stderr, "pcap error: %s\n", errbuf);
        return 1;
    }

    printf("[*] WiFi Analyzer started on %s\n", IFACE);
    load_vendors("vendors.csv");
    printf("Vendors loaded\n");

    pcap_loop(handle, -1, handle_packet, NULL);

    pcap_close(handle);
    return 0;
}

