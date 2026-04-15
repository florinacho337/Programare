IFACE="wlp2s0"

echo "[*] Setting $IFACE to MONITOR mode"

sudo ip link set $IFACE down
sudo iw dev $IFACE set type monitor
sudo ip link set $IFACE up

echo "[+] $IFACE is now in MONITOR mode"
