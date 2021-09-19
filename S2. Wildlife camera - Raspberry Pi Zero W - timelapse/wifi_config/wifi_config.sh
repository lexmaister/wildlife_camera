#! /bin/bash

arg1=$1

if [ $arg1 == "ap" ] ; then
    cp /etc/dhcpcd.ap.conf /etc/dhcpcd.conf  &&
    systemctl daemon-reload &&
    service dhcpcd restart &&
    systemctl start dnsmasq &&
    systemctl start hostapd &&
    systemctl enable dnsmasq &&
    systemctl enable hostapd
elif [ $arg1 == "wifi" ] ; then
    systemctl stop dnsmasq &&
    systemctl stop hostapd &&
    systemctl disable dnsmasq &&
    systemctl disable hostapd &&
    cp /etc/dhcpcd.wifi.conf /etc/dhcpcd.conf &&
    systemctl daemon-reload &&
    service dhcpcd restart
else
    echo "UNKNOWN input"
fi
