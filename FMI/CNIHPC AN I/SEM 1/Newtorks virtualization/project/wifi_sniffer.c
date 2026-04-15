#include <pcap.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <arpa/inet.h>
#include <ctype.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <endian.h>

#define IFACE "wlp2s0"
#define HOP_INTERVAL 2

/* ================= STRUCTURI ================= */

struct ieee80211_hdr {
    uint16_t fc;          // Frame Control (16 biți)
                          // Conține:
                          //  - versiunea protocolului
                          //  - tipul frame-ului (Management / Control / Data)
                          //  - subtipul (Beacon, Data, ACK etc.)
                          //  - flag-uri: To DS, From DS, Retry, Privacy, etc.

    uint16_t dur;         // Duration / ID
                          // Timpul (în microsecunde) rezervat pe mediu
                          // sau Association ID în anumite frame-uri

    uint8_t addr1[6];     // Address 1
                          // De obicei: destinația (Receiver Address)

    uint8_t addr2[6];     // Address 2
                          // De obicei: sursa (Transmitter Address)
                          // Pentru Beacon: BSSID-ul AP-ului

    uint8_t addr3[6];     // Address 3
                          // De obicei: BSSID sau adresa finală
                          // (depinde de To DS / From DS)

    uint16_t seq;         // Sequence Control
                          // Conține:
                          //  - număr de secvență (fragmentare / reordonare)
                          //  - număr fragment
};


struct llc_hdr {
    uint8_t dsap;         // Destination Service Access Point
                          // De obicei 0xAA pentru SNAP

    uint8_t ssap;         // Source Service Access Point
                          // De obicei 0xAA pentru SNAP

    uint8_t ctrl;         // Control field
                          // De obicei 0x03 (Unnumbered Information)

    uint8_t oui[3];       // Organizationally Unique Identifier
                          // 0x00 0x00 0x00 → indică Ethernet encapsulation

    uint16_t ethertype;   // EtherType
                          // Identifică protocolul superior:
                          //  - 0x0800 → IPv4
                          //  - 0x86DD → IPv6
                          //  - 0x0806 → ARP
};


struct eth_hdr {
    uint8_t dst[6];       // Destination MAC Address
                          // Adresa MAC a destinatarului

    uint8_t src[6];       // Source MAC Address
                          // Adresa MAC a sursei

    uint16_t ethertype;   // EtherType
                          // Identifică protocolul superior:
                          //  - 0x0800 → IPv4
                          //  - 0x86DD → IPv6
                          //  - 0x0806 → ARP
};

struct ip_hdr {
    uint8_t ver_ihl;      // Version + IHL (Internet Header Length)
                          //  - primii 4 biți: versiunea IP (4)
                          //  - următorii 4 biți: lungimea headerului (în words de 4 bytes)

    uint8_t tos;          // Type of Service
                          // Prioritate / QoS (DSCP, ECN)

    uint16_t tot_len;     // Total Length
                          // Lungimea totală a pachetului IP (header + payload) în bytes

    uint16_t id;          // Identification
                          // ID folosit pentru reasamblarea fragmentelor

    uint16_t frag_off;    // Fragment Offset + Flags
                          // Indică fragmentarea pachetului IP

    uint8_t ttl;          // Time To Live
                          // Număr maxim de hop-uri
                          // Scade cu 1 la fiecare router

    uint8_t proto;        // Protocol
                          // Protocolul superior:
                          //  - 6 → TCP
                          //  - 17 → UDP
                          //  - 1 → ICMP

    uint16_t checksum;    // Header Checksum
                          // Verifică integritatea headerului IP

    uint32_t src;         // Source IP Address
                          // Adresa IP sursă

    uint32_t dst;         // Destination IP Address
                          // Adresa IP destinație
};

struct tcp_hdr {
    uint16_t src_port;    // Source Port
                          // Portul aplicației sursă (ex: 443, 80)

    uint16_t dst_port;    // Destination Port
                          // Portul aplicației destinație

    uint32_t seq;         // Sequence Number
                          // Numărul primului byte din segment

    uint32_t ack;         // Acknowledgment Number
                          // Confirmă primirea datelor

    uint8_t offset_reserved;
                          // Data Offset (lungimea headerului TCP)
                          // + biți rezervați

    uint8_t flags;        // TCP Flags
                          // SYN, ACK, FIN, RST, PSH, URG

    uint16_t window;      // Window Size
                          // Controlul fluxului (câți bytes pot fi trimiși)

    uint16_t checksum;    // TCP Checksum
                          // Verifică integritatea headerului + payload

    uint16_t urg_ptr;     // Urgent Pointer
                          // Folosit când flag-ul URG este setat
};

/* ================= UTIL ================= */

void mac_to_json(const char *label, const uint8_t *mac, char *out, int size) {
    snprintf(out, size, "\"%s\":\"%02x:%02x:%02x:%02x:%02x:%02x\"",
             label, mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
}

const char* ip_proto_to_str(uint8_t proto) {
    switch (proto) {
        case 1:  return "ICMP";
        case 2:  return "IGMP";
        case 6:  return "TCP";
        case 17: return "UDP";
        case 47: return "GRE";
        case 50: return "ESP";
        case 51: return "AH";
        case 89: return "OSPF";
        default: return "UNKNOWN";
    }
}

void tcp_flags_to_json(uint8_t flags, char *out, int size) {
    out[0] = 0;
    int first = 1;
    if (flags & 0x01) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"FIN\"",size-strlen(out)-1); first=0; }
    if (flags & 0x02) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"SYN\"",size-strlen(out)-1); first=0; }
    if (flags & 0x04) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"RST\"",size-strlen(out)-1); first=0; }
    if (flags & 0x08) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"PSH\"",size-strlen(out)-1); first=0; }
    if (flags & 0x10) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"ACK\"",size-strlen(out)-1); first=0; }
    if (flags & 0x20) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"URG\"",size-strlen(out)-1); first=0; }
    if (flags & 0x40) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"ECE\"",size-strlen(out)-1); first=0; }
    if (flags & 0x80) { if(!first) strncat(out, ",", size-strlen(out)-1); strncat(out,"\"CWR\"",size-strlen(out)-1); first=0; }
}

void ip_to_json(struct ip_hdr *ip, char *out, int size) {
    char src[INET_ADDRSTRLEN], dst[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &ip->src, src, sizeof(src));
    inet_ntop(AF_INET, &ip->dst, dst, sizeof(dst));
    snprintf(out, size,
        "{\"version\":%d,\"ihl\":%d,\"tot_len\":%d,\"id\":%d,"
        "\"ttl\":%d,\"protocol\":\"%s\",\"src\":\"%s\",\"dst\":\"%s\"}",
        ip->ver_ihl>>4, (ip->ver_ihl & 0x0F)*4, ntohs(ip->tot_len), ntohs(ip->id),
        ip->ttl, ip_proto_to_str(ip->proto), src, dst);
}

void tcp_to_json(struct tcp_hdr *tcp, char *out, int size) {
    char flags_str[128];
    tcp_flags_to_json(tcp->flags, flags_str, sizeof(flags_str));

    snprintf(out, size,
        "{\"src_port\":%d,\"dst_port\":%d,\"seq\":%u,\"ack\":%u,"
        "\"flags\":[%s],\"window\":%d}",
        ntohs(tcp->src_port), ntohs(tcp->dst_port),
        ntohl(tcp->seq), ntohl(tcp->ack),
        flags_str, ntohs(tcp->window));
}

void http_to_json(const uint8_t *data, int len, char *out, int size) {
    char buf[4096];
    int j = 0;

    for (int i = 0; i < len && j < (int)(sizeof(buf) - 1); i++) {
        char c = data[i];

        if (c == '"' || c == '\\') {
            if (j + 2 < (int)sizeof(buf)) {
                buf[j++] = '\\';
                buf[j++] = c;
            }
        } else if (c >= 32 && c <= 126) {
            buf[j++] = c;
        } else {
            if (j + 6 < (int)sizeof(buf)) {
                j += snprintf(buf + j, sizeof(buf) - j, "\\u%04x", (unsigned char)c);
            }
        }
    }

    buf[j] = 0;  // terminare string
    snprintf(out, size, "{\"payload\":\"%s\"}", buf);
}

// Return values:
// 0 = frame invalid / prea scurt
// 1 = frame Data + IP/LLC/etc. decodabil
// 2 = frame Data, dar criptat sau fără IP/LLC
int parse_monitor_l2(const struct pcap_pkthdr *header,
                     const uint8_t *packet,
                     const uint8_t **ptr_out,
                     uint8_t *src_mac,
                     uint8_t *dst_mac)
{
    const uint8_t *ptr = packet;

    /* ================= Radiotap ================= */
    if (header->caplen < 4)
        return 0;

    uint16_t rt_len = le16toh(*(uint16_t *)(packet + 2));
    if (rt_len >= header->caplen)
        return 0;

    ptr += rt_len;

    /* ================= 802.11 header ================= */
    if (ptr + 24 > packet + header->caplen)
        return 0;

    const struct ieee80211_hdr *wifi = (const struct ieee80211_hdr *)ptr;
    uint16_t fc = le16toh(wifi->fc);

    int type = (fc >> 2) & 0x3;
    if (type != 2)  // nu e Data frame
        return 0;

    int to_ds   = (fc >> 8) & 1;
    int from_ds = (fc >> 9) & 1;

    /* Extragem adresele brute */
    const uint8_t *addr1 = wifi->addr1;
    const uint8_t *addr2 = wifi->addr2;
    const uint8_t *addr3 = wifi->addr3;
    const uint8_t *addr4 = NULL;

    int hdr_len = 24;

    if (to_ds && from_ds) {
        if (ptr + 30 > packet + header->caplen)
            return 0;
        addr4 = ptr + 24;
        hdr_len += 6;
    }

    int qos = ((fc >> 4) & 0xF) == 8;
    if (qos)
        hdr_len += 2;

    /* ================= Determinare SRC / DST ================= */
    if (!to_ds && !from_ds) {
        // STA ↔ STA (IBSS / mgmt)
        memcpy(dst_mac, addr1, 6);
        memcpy(src_mac, addr2, 6);
    }
    else if (!to_ds && from_ds) {
        // AP → STA
        memcpy(dst_mac, addr1, 6);
        memcpy(src_mac, addr3, 6);
    }
    else if (to_ds && !from_ds) {
        // STA → AP
        memcpy(dst_mac, addr3, 6);
        memcpy(src_mac, addr2, 6);
    }
    else {
        // WDS (AP ↔ AP)
        if (!addr4)
            return 0;
        memcpy(dst_mac, addr3, 6);
        memcpy(src_mac, addr4, 6);
    }

    ptr += hdr_len;

    /* ================= LLC ================= */
    if (ptr + sizeof(struct llc_hdr) > packet + header->caplen)
        return 2;  // Data frame, dar fără IP

    const struct llc_hdr *llc = (const struct llc_hdr *)ptr;

    if (llc->dsap != 0xAA || llc->ssap != 0xAA)
        return 2;

    if (ntohs(llc->ethertype) != 0x0800) //IPv4
        return 2;

    *ptr_out = ptr + sizeof(struct llc_hdr);
    return 1;
}

int parse_managed_l2(const struct pcap_pkthdr *header,
                     const uint8_t *packet,
                     const uint8_t **ptr_out,
                     uint8_t *src_mac,
                     uint8_t *dst_mac)
{
    if (header->caplen < sizeof(struct eth_hdr))
        return 0;

    struct eth_hdr *eth = (struct eth_hdr *)packet;

    memcpy(src_mac, eth->src, 6);
    memcpy(dst_mac, eth->dst, 6);

    if (ntohs(eth->ethertype) != 0x0800) // IPv4
        return 0;

    *ptr_out = packet + sizeof(struct eth_hdr);
    return 1;
}

void packet_to_json(uint8_t *src_mac, uint8_t *dst_mac,
                    struct ip_hdr *ip, struct tcp_hdr *tcp,
                    uint8_t *http_payload, int payload_len)
{
    char mac_src[64], mac_dst[64], ip_json[512], tcp_json[512], http_json[4096];

    mac_to_json("src_mac", src_mac, mac_src, sizeof(mac_src));
    mac_to_json("dst_mac", dst_mac, mac_dst, sizeof(mac_dst));

    if (ip)
        ip_to_json(ip, ip_json, sizeof(ip_json));
    if (tcp)
        tcp_to_json(tcp, tcp_json, sizeof(tcp_json));
    if (http_payload)
        http_to_json(http_payload, payload_len, http_json, sizeof(http_json));

    printf("{\"type\":\"packet\",%s,%s,", mac_src, mac_dst);
    printf("\"ip\":%s,", ip ? ip_json : "null");
    printf("\"tcp\":%s,", tcp ? tcp_json : "null");
    printf("\"http\":%s", http_payload ? http_json : "null");
    printf("}\n");
    fflush(stdout);
}

/* ================= CHANNEL HOPPER ================= */

void* channel_hopper(void* arg) {
    int channels[] = {1,2,3,4,5,6,7,8,9,10,11,12,13};
    int n = sizeof(channels)/sizeof(channels[0]);
    int i = 0;
    char cmd[128];

    while (1) {
        sprintf(cmd, "iw dev %s set channel %d", IFACE, channels[i]);
        system(cmd);
        i = (i + 1) % n;
        sleep(HOP_INTERVAL);
    }
}

/* ================= PACKET HANDLER ================= */

void handle_packet(u_char *args,
                   const struct pcap_pkthdr *header,
                   const u_char *packet)
{
    const uint8_t *ptr = packet;
    int monitor_mode = *(int*)args;
    uint8_t src_mac[6], dst_mac[6];

    // ================= L2 =================
    if (monitor_mode) {
        int res = parse_monitor_l2(header, packet, &ptr, src_mac, dst_mac);

	if (res == 0) return;          // frame invalid
	if (res == 2) {                 // criptat / fără IP/TCP
    	    packet_to_json(src_mac, dst_mac, NULL, NULL, NULL, 0);
    	    return;
	}
    } else {
        if (!parse_managed_l2(header, packet, &ptr, src_mac, dst_mac)) {
            packet_to_json(src_mac, dst_mac, NULL, NULL, NULL, 0);
            return;
        }
    }

    // ================= IP =================
    struct ip_hdr *ip = NULL;
    if (header->caplen < ptr - packet + sizeof(struct ip_hdr))
        return;

    ip = (struct ip_hdr *)ptr;
    int ip_len = (ip->ver_ihl & 0x0F) * 4;
    if (header->caplen < ptr - packet + ip_len)
        return;
    ptr += ip_len;

    // ================= TCP =================
    struct tcp_hdr *tcp = NULL;
    int tcp_len = 0;
    if (ip->proto == 6) { // TCP
        if (header->caplen < ptr - packet + sizeof(struct tcp_hdr))
            return;
        tcp = (struct tcp_hdr *)ptr;
        tcp_len = ((tcp->offset_reserved >> 4) & 0xF) * 4;
        if (header->caplen < ptr - packet + tcp_len)
            return;
        ptr += tcp_len;
    }

    // ================= HTTP =================
    int payload_len = header->caplen - (ptr - packet);
    uint8_t *http_payload = NULL;
    if (tcp && ntohs(tcp->dst_port) == 80 && payload_len > 0)
        http_payload = (uint8_t *)ptr;

    // ================= JSON =================
    packet_to_json(src_mac, dst_mac, ip, tcp, http_payload, payload_len);
}

/* ================= MAIN ================= */

int main() {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle;
    int monitor_mode = 0;

    handle = pcap_open_live(IFACE, BUFSIZ, 1, 1000, errbuf);
    if (!handle) {
        fprintf(stderr, "pcap error: %s\n", errbuf);
        return 1;
    }

    int dlt = pcap_datalink(handle);
    if (dlt == DLT_IEEE802_11_RADIO) {
        monitor_mode = 1;
        pthread_t t;
        pthread_create(&t, NULL, channel_hopper, NULL);
    }

    printf("[*] Sniffer started (%s mode)\n",
           monitor_mode ? "MONITOR" : "MANAGED");

    pcap_loop(handle, -1, handle_packet, (u_char*)&monitor_mode);
    pcap_close(handle);
}

