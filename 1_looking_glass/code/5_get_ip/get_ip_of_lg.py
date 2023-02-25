import dpkt
import socket
# import datetime
import sys
import os
import pickle
import operator
import ast
import json
from pytz import timezone
import settings

DST_DIR = settings.DST_DIR
LG_LIST = settings.LG_LIST
RESULT_DIR = settings.RESULT_DIR
MACHINE_IPS = settings.MACHINE_IPS
LG_NUM = len(LG_LIST)

result_each_time = []

for m_idx in range(0, len(MACHINE_IPS)):

    time_list = []
    with open(f'{RESULT_DIR}/{m_idx}_send.txt', 'r') as srcfile:
        for row in srcfile:
            time_list.append(float(row.strip()))

    assert(len(time_list) == LG_NUM+1)

    ip_count_list = [{} for idx in range(LG_NUM)]

    now_idx = 0
    with open(f'{RESULT_DIR}/{m_idx}_receive.pcap', 'rb') as fr:
        pcap = dpkt.pcap.Reader(fr)
        for timestamp, buffer in pcap:
            if timestamp > time_list[-1]: break

            for idx in range(now_idx, LG_NUM):
                if time_list[idx] < timestamp < time_list[idx+1]:
                    now_idx = idx
                    break

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
            this_ip = src_ip if src_ip != MACHINE_IPS[m_idx] else dst_ip
            if this_ip not in ip_count_list[now_idx]:
                ip_count_list[now_idx][this_ip] = 0
            ip_count_list[now_idx][this_ip] += 1

    result_each_time.append(ip_count_list)

dict_lg_info = {}
for lg_idx in range(LG_NUM):
    set_list = []
    for m_idx in range(len(MACHINE_IPS)):
        set_list.append(set(result_each_time[m_idx][lg_idx].keys()))
        print(result_each_time[m_idx][lg_idx])
    candiates = list(set.intersection(*set_list))
    print(candiates)
    print('----------------------')
    if len(candiates) == 1:
        dict_lg_info[candiates[0]] = LG_LIST[lg_idx]

print('dst: ', len(dict_lg_info))

pickle.dump(dict_lg_info, open(f'{DST_DIR}/dict_lg_info.bin', 'wb'))
