import dpkt
import socket
# import datetime
import os
import pickle
import operator
import ast
import json
from pytz import timezone

LG_DIR = '../../'
FORMER_RESULT_DIR = '../4_filter_by_api/result'

# 1. use api to geolocate successfully
# 2. cannot use api
DST_FILES_DIR = f'{LG_DIR}/pickle_bin/'
os.system(f'mkdir -p {DST_FILES_DIR}')

input_list = pickle.load(open(f'{FORMER_RESULT_DIR}/list_good_routers.bin', 'rb'))
time_list = []
with open('./send.txt', 'r') as srcfile:
    for row in srcfile:
        time_0 = float(row.split('\t')[0])
        time_1 = float(row.split('\t')[1])
        time_list.append((time_0, time_1))

LG_NUM = len(input_list)
MAX_TIMESTAMP = time_list[-1][-1]

ip_count_list = [{} for idx in range(LG_NUM)]

now_idx = 0
MACHINE_IP = '198.13.38.108'
with open('./receive.pcap', 'rb') as fr:
    pcap = dpkt.pcap.Reader(fr)
    for timestamp, buffer in pcap:
        if timestamp > MAX_TIMESTAMP: 
            print(timestamp)
            break

        is_good = False
        for idx in range(now_idx, LG_NUM):
            if time_list[idx][0] < timestamp < time_list[idx][1]:
                is_good = True
                now_idx = idx
                break

        if not is_good: continue

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
        if this_ip not in ip_count_list[now_idx]:
            ip_count_list[now_idx][this_ip] = 0
        ip_count_list[now_idx][this_ip] += 1

def get_ip_from_dict(dict_ip_count):
    if len(dict_ip_count):
        candiate_ip = max(dict_ip_count, key=dict_ip_count.get)
        if dict_ip_count[candiate_ip] < 2:
            return None
        for ip in dict_ip_count:
            if ip == candiate_ip: continue
            if int(dict_ip_count[candiate_ip] / dict_ip_count[ip]) < 3:
                return None
        return candiate_ip
    return None

bad_idx = []
for idx, ip_count in enumerate(ip_count_list):
    ip = get_ip_from_dict(ip_count)
    if ip:
        print(ip_count)
    else:
        bad_idx.append(idx)

print(bad_idx)

