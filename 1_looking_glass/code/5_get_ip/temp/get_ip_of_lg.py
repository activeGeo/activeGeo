import dpkt
import socket
# import datetime
import os
import pickle
import operator
import ast
import json
from pytz import timezone


now_idx = 0
MACHINE_IP = '198.13.38.108'
with open('./output_2.pcap', 'rb') as fr:
    pcap = dpkt.pcap.Reader(fr)
    for timestamp, buffer in pcap:

        # 解包, 物理层
        ethernet = dpkt.ethernet.Ethernet(buffer)
        # 判断网络层是否存在
        if not isinstance(ethernet.data, dpkt.ip.IP):
            continue
        ip = ethernet.data
        # 判断是否是 ICMP
        if not isinstance(ip.data, dpkt.icmp.ICMP):
            continue

        icmp = ip.data
        src_ip = socket.inet_ntoa(ip.src)
        dst_ip = socket.inet_ntoa(ip.dst)
        this_ip = src_ip if src_ip != MACHINE_IP else dst_ip
        print(timestamp, this_ip)

