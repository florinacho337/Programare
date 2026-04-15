import gi
import json
import subprocess
import threading

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk, Pango

ANALYZER_BIN = "./wifi_analyzer"
SNIFFER_BIN  = "./wifi_sniffer"
RSSI_MIN = -95
RSSI_MAX = -30

class WiFiAnalyzer(Gtk.Window):
    def __init__(self):
        super().__init__(title="WiFi Analyzer")
        self.analyzer_proc = None
        self.sniffer_proc = None
        self.set_default_size(1400, 800)

        self.networks = {}  # key = BSSID

        notebook = Gtk.Notebook()
        self.add(notebook)

        # TAB 1: Network list
        # Index: 0 (icon)    1 (SSID) 2 (BSSID) 3 (Vendor) 4 (RSSI-str) 5 (Channel) 6 (Freq) 7 (Sec)
        self.store = Gtk.ListStore(GdkPixbuf.Pixbuf, str, str, str, str, int, str, str)
        self.tree = Gtk.TreeView(model=self.store)
        renderer_pix = Gtk.CellRendererPixbuf()
        col_pix = Gtk.TreeViewColumn("", renderer_pix, pixbuf=0)
        self.tree.append_column(col_pix)

        headers = ["SSID", "BSSID", "Vendor", "RSSI", "Channel", "Freq", "Security"]
        for i, title in enumerate(headers):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=i+1)
            self.tree.append_column(column)

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.tree)
        notebook.append_page(scroll, Gtk.Label(label="Networks"))

        # TAB 2: Channel graph
        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw_channels)
        self.darea.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
        self.darea.connect("motion-notify-event", self.on_motion)
        notebook.append_page(self.darea, Gtk.Label(label="Channels"))
        
        # TAB 3: Sniffer
        self.sniffer_store = Gtk.ListStore(
            str,  # SRC MAC
            str,  # DST MAC
            str,  # SRC IP
            str,  # SRC PORT
            str,  # DST IP
            str,  # DST PORT
            str,  # FLAGS
            str,  # HTTP
            object
        )

        self.sniffer_tree = Gtk.TreeView(model=self.sniffer_store)

        headers = ["SRC MAC", "DST MAC", "SRC IP", "SRC PORT", "DST IP", "DST PORT", "Flags", "HTTP"]
        for i, title in enumerate(headers):
            renderer = Gtk.CellRendererText()
            renderer.set_property("wrap-width", 300)
            renderer.set_property("wrap-mode", Pango.WrapMode.WORD_CHAR)
            column = Gtk.TreeViewColumn(title, renderer, text=i)
            column.set_resizable(True)
            self.sniffer_tree.append_column(column)

        sniffer_scroll = Gtk.ScrolledWindow()
        sniffer_scroll.add(self.sniffer_tree)

        notebook.append_page(sniffer_scroll, Gtk.Label(label="Sniffer"))
        
        self.sniffer_tree.connect("row-activated", self.on_packet_expand)

        self.notebook = notebook
        notebook.connect("switch-page", self.on_tab_changed)

        # WiFi icons
        self.icon_wifi_green = GdkPixbuf.Pixbuf.new_from_file("files/wifi_green.png")
        self.icon_wifi_yellow = GdkPixbuf.Pixbuf.new_from_file("files/wifi_yellow.png")
        self.icon_wifi_red = GdkPixbuf.Pixbuf.new_from_file("files/wifi_red.png")

        GLib.timeout_add(1000, self.refresh)
        
        self.start_analyzer()

    # ================= ICON =================
    def rssi_icon(self, rssi):
        if rssi > -60:
            return self.icon_wifi_green
        elif rssi > -75:
            return self.icon_wifi_yellow
        return self.icon_wifi_red

    # ================= DATA =================
    def read_loop(self, pipe):
        for line in pipe:
            try:
                msg = json.loads(line)
                GLib.idle_add(self.dispatch_message, msg)
            except json.JSONDecodeError:
                pass
                
    def dispatch_message(self, msg):
        msg_type = msg.get("type")

        if msg_type == "network":
            self.update_network(msg)
        elif msg_type == "packet":
            self.update_sniffer(msg)

        return False

    def get_best_networks_by_ssid(self):
        ssid_map = {}

        for net in self.networks.values():
            ssid = net["ssid"] if net["ssid"] else "<hidden>"

            if ssid not in ssid_map:
                ssid_map[ssid] = net
            else:
                if net["rssi"] > ssid_map[ssid]["rssi"]:
                    ssid_map[ssid] = net

        return ssid_map.values()

    def refresh_ui(self):
        self.store.clear()
        for net in self.get_best_networks_by_ssid():
            self.store.append([
                self.rssi_icon(net["rssi"]),
                net["ssid"] if net["ssid"] else "<hidden>",
                net["bssid"],
                net["vendor"],
                f'{net["rssi"]} dBm',
                net["channel"],
                f'{net["freq"]} MHz',
                net["security"]
            ])

    def update_network(self, net):
        bssid = net["bssid"]
        self.networks[bssid] = net

        self.refresh_ui()
        return False

    def update_sniffer(self, pkt):
        src_mac = pkt.get("src_mac", "")
        dst_mac = pkt.get("dst_mac", "")

        ip = pkt["ip"] or {}
        src_ip = ip.get("src", "x")
        dst_ip = ip.get("dst", "x")

        tcp = pkt.get("tcp") or {}
        src_port = "x"
        dst_port = "x"
        flags = "x"
        if tcp:
            src_port = str(tcp.get("src_port", ""))
            dst_port = str(tcp.get("dst_port", ""))
            flags = ",".join(tcp.get("flags", []))

        http = pkt.get("http") or {}
        http_payload = http.get("payload", "") if http else ""

        self.sniffer_store.append([
            src_mac,
            dst_mac,
            src_ip,
            src_port,
            dst_ip,
            dst_port,
            flags,
            http_payload,
            pkt
        ])

        # păstrăm maxim 1000 de pachete
        if len(self.sniffer_store) > 1000:
            self.sniffer_store.remove(self.sniffer_store.get_iter_first())

    def refresh(self):
        self.darea.queue_draw()
        return True

    def on_packet_expand(self, tree, path, _):
        model = tree.get_model()
        row = model[path]

        # Se extrage JSON-ul original
        pkt_json = row[8]

        text_lines = ["MAC:", f"  - SRC: {row[0]}", f"  - DST: {row[1]}"]

        ip = pkt_json.get("ip")
        if ip:
            text_lines.append("\nIP:")
            text_lines.append(f"  - Version: {ip.get('version', '')}")
            text_lines.append(f"  - ID: {ip.get('id', '')}")
            text_lines.append(f"  - IHL: {ip.get('ihl', '')} bytes")
            text_lines.append(f"  - Total Length: {ip.get('tot_len', '')} bytes")
            text_lines.append(f"  - SRC IP: {ip.get('src', '')}")
            text_lines.append(f"  - DST IP: {ip.get('dst', '')}")
            text_lines.append(f"  - Protocol: {ip.get('protocol', '')}")
            text_lines.append(f"  - TTL: {ip.get('ttl', '')}")

        tcp = pkt_json.get("tcp")
        if tcp:
            text_lines.append("\nTCP:")
            text_lines.append(f"  - SRC PORT: {tcp.get('src_port', '')}")
            text_lines.append(f"  - DST PORT: {tcp.get('dst_port', '')}")
            text_lines.append(f"  - Flags: {','.join(tcp.get('flags', []))}")
            text_lines.append(f"  - Seq: {tcp.get('seq', '')}")
            text_lines.append(f"  - Ack: {tcp.get('ack', '')}")
            text_lines.append(f"  - Window: {tcp.get('window', '')} bytes")

        http = pkt_json.get("http")
        if http:
            text_lines.append("\nHTTP:")
            text_lines.append(http.get("payload", ""))

        text = "\n".join(text_lines)

        dialog = Gtk.Dialog(
            title="Packet details",
            transient_for=self,
            flags=0
        )
        dialog.set_default_size(700, 500)
        dialog.add_button("Close", Gtk.ResponseType.CLOSE)

        label = Gtk.Label(label=text)
        label.set_xalign(0)
        label.set_yalign(0)
        label.set_selectable(True)
        label.set_line_wrap(True)

        scrolled = Gtk.ScrolledWindow()
        scrolled.add(label)

        dialog.get_content_area().pack_start(scrolled, True, True, 0)
        dialog.show_all()
        dialog.run()
        dialog.destroy()


    # ================= CHANNEL GRAPH =================
    def get_overlap_channels(self, ch, bw):
        if bw <= 20:
            # 20 MHz (ocupa 5 canale: 2 jos, 2 sus, 1 centru. Ex: Ch 6 -> 4, 5, 6, 7, 8)
            return range(max(1, ch - 2), min(14, ch + 3))
        elif bw == 40:
            # 40 MHz (ocupa 9 canale: 4 jos, 4 sus, 1 centru. Ex: Ch 6 -> 2-10)
            return range(max(1, ch - 4), min(14, ch + 5))
        return range(ch, ch + 1)  # Fallback la un singur canal

    def scale_rssi(self, rssi, height):
        rssi_clamped = max(RSSI_MIN, min(RSSI_MAX, rssi))
        scale = (rssi_clamped - RSSI_MIN) / (RSSI_MAX - RSSI_MIN)
        return height - 30 - scale * (height - 40)

    def rssi_color(self, rssi):
        if rssi > -55: return (0, 1, 0, 0.5)
        elif rssi > -75: return (1, 1, 0, 0.5)
        return (1, 0, 0, 0.5)

    def on_draw_channels(self, widget, cr):
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()

        # background
        cr.set_source_rgb(.12, .12, .12)
        cr.paint()

        # axes
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(1)
        cr.move_to(50, 10)
        cr.line_to(50, height-30)
        cr.line_to(width-10, height-30)
        cr.stroke()

        # y-axis labels
        for val in [RSSI_MAX, -40, -50, -60, -70, -80, -90, RSSI_MIN]:
            y = self.scale_rssi(val, height)

            cr.set_source_rgb(1, 1, 1)
            cr.move_to(10, y)
            cr.show_text(f'{val} dBm')

            cr.set_source_rgba(1, 1, 1, 0.15)
            cr.move_to(50, y)
            cr.line_to(width - 10, y)
            cr.stroke()

        # x-axis channels
        for ch in range(1, 14):
            x = 50 + ch*(width-100)/13

            cr.set_source_rgb(1, 1, 1)
            cr.move_to(x, height-30)
            cr.line_to(x, height-25)
            cr.stroke()

            cr.set_source_rgb(1, 1, 1)
            cr.move_to(x-5, height-10)
            cr.show_text(str(ch))

        cr.save()
        cr.rectangle(50, 10, width - 60, height - 40)
        cr.clip()

        # networks
        for net in self.networks.values():
            self.draw_network(cr, net, width, height)

        cr.restore()

    def draw_network(self, cr, net, width, height):
        ch = net["channel"]
        rssi = net["rssi"]
        bw = net["bandwidth"]
        if ch < 1 or ch > 13: return

        channel_width_px = (width - 100) / 13
        # Calculul lățimii clopotului în pixeli (bw_px)
        if bw >= 40:
            # Rețelele 40 MHz ocupa ~9 canale (4.5 de fiecare parte)
            bw_px = 4.5 * channel_width_px
        else:
            # Rețelele 20 MHz ocupa ~5 canale (2.5 de fiecare parte)
            bw_px = 2.5 * channel_width_px

        center_x = 50 + ch*(width-100)/13
        peak_y = self.scale_rssi(rssi, height)
        color = self.rssi_color(rssi)

        cr.set_source_rgba(*color)
        cr.move_to(center_x-bw_px, height-30)
        cr.curve_to(center_x-bw_px/2, peak_y,
                    center_x+bw_px/2, peak_y,
                    center_x+bw_px, height-30)
        cr.close_path()
        cr.fill()

    # ================= HOVER TOOLTIP =================
    def on_motion(self, widget, event):
        x = event.x
        ssids_to_show = []
        width = widget.get_allocated_width()
        channel_width_px = (width - 100) / 13

        for ch in range(1, 14):
            center_x = 50 + ch * channel_width_px
            if center_x - channel_width_px / 2 <= x <= center_x + channel_width_px / 2:
                # toate rețelele pe canalul ch
                ssids_to_show = []
                for net in self.networks.values():
                    net_ch = net["channel"]
                    net_bw = net["bandwidth"]

                    overlap_range = self.get_overlap_channels(net_ch, net_bw)

                    if ch in overlap_range:
                        ssids_to_show.append(f'{net["ssid"] if net["ssid"] else "<hidden>"} ({net["rssi"]} dBm)')
                break
        if ssids_to_show:
            widget.set_tooltip_text("\n".join(ssids_to_show))
        else:
            widget.set_tooltip_text(None)
            
    # ========= COMUTATOR ANALYZER ↔ SNIFFER ============
    def start_analyzer(self):
        if self.analyzer_proc:
            return
        self.analyzer_proc = subprocess.Popen(
            [ANALYZER_BIN], stdout=subprocess.PIPE, text=True
        )
        threading.Thread(
            target=self.read_loop,
            args=(self.analyzer_proc.stdout,),
            daemon=True
        ).start()

    def stop_analyzer(self):
        if self.analyzer_proc:
            self.analyzer_proc.terminate()
            self.analyzer_proc = None

    def start_sniffer(self):
        if self.sniffer_proc:
            return
        self.sniffer_proc = subprocess.Popen(
            [SNIFFER_BIN], stdout=subprocess.PIPE, text=True
        )
        threading.Thread(
            target=self.read_loop,
            args=(self.sniffer_proc.stdout,),
            daemon=True
        ).start()

    def stop_sniffer(self):
        if self.sniffer_proc:
            self.sniffer_proc.terminate()
            self.sniffer_proc = None
            
    def on_tab_changed(self, notebook, page, index):
        # 0 = Networks, 1 = Channels
        if index in (0, 1):
            self.stop_sniffer()
            self.start_analyzer()
        # 2 = Sniffer
        elif index == 2:
            self.stop_analyzer()
            self.start_sniffer()

def main():
    win = WiFiAnalyzer()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
