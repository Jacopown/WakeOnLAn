import click
import re
import socket

# Checks validity of mac address


def macAddressType(argValue):
    pattern = re.compile('^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$')
    if not pattern.match(argValue):
        raise click.BadParameter
    return argValue

# Checks validity of ipv4 address


def ipAddressType(argValue):
    parts = argValue.split(".")

    if len(parts) != 4:
        raise click.BadParameter

    for part in parts:
        if not isinstance(int(part), int):
            raise click.BadParameter

        if int(part) < 0 or int(part) > 255:
            raise click.BadParameter

        if re.compile('^0[0-9]$').match(part) or re.compile('^00[0-9]$').match(part):
            raise click.BadParameter

    return argValue


# main

@click.command()
@click.argument('mac-address')
@click.option('-ip', '--ip-address', default='192.168.1.255', help='your local broadcast ip address')
def wake(mac_address, ip_address):
    '''This script wakes your device through LAN'''
    mac_address = macAddressType(mac_address)
    ip_address = ipAddressType(ip_address)
    # Generating magic packet
    macElements = mac_address.split(':')
    packet = ['0xFF']*6
    for i in range(len(macElements)):
        macElements[i] = int('0x'+macElements[i], 16)
        packet[i] = int(packet[i], 16)
    for i in range(16):
        for j in range(6):
            packet.append(macElements[j])

    # Sending magic packet to broadcast ip

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(bytes(packet), (ip_address, 7))
