IFACE="wlp2s0"

echo "[*] Setting $IFACE to MANAGED mode"

sudo ip link set $IFACE down
sudo iw dev $IFACE set type managed
sudo ip link set $IFACE up

echo "[+] $IFACE is now in MANAGED mode"
