#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:filter_data.py
@time:2018/07/22

Prepocss train.csv, add distance and speed, and filter data
"""

import csv
from math import radians, tan, atan, sin, cos, acos

def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = radians(float(latA))
    radLonA = radians(float(lonA))
    radLatB = radians(float(latB))
    radLonB = radians(float(lonB))

    pA = atan(rb / ra * tan(radLatA))
    pB = atan(rb / ra * tan(radLatB))
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    c1 = (sin(x) - x) * (sin(pA) + sin(pB)) ** 2 / (cos(x / 2) ** 2 + 0.00000000001)
    c2 = (sin(x) + x) * (sin(pA) - sin(pB)) ** 2 / (sin(x / 2) ** 2 + 0.0000000001)
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    return distance

def compute_dis_speed(old_file, new_file):
    csvfile_w = open(new_file, "w")
    writer = csv.writer(csvfile_w)
    idx = 0
    with open(old_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # if idx > 1: break
            if idx == 0:
                row.append('trip_distance')
                row.append('trip_speed')
            else:
                start_lon = float(row[5])
                start_lat = float(row[6])
                end_lon = float(row[7])
                end_lat = float(row[8])
                dura = float(row[-1])
                try:
                    dis = getDistance(start_lat, start_lon, end_lat, end_lon)
                except ValueError:
                    dis = -1
                    speed = -1
                else:
                    speed = (dis * 1.0) / dura
                row.append(str(dis))
                row.append(str(speed))

            idx += 1
            writer.writerow(row)
    csvfile_w.close()

def filter_dura_dis_speed(old_file, new_file):
    csvfile_w = open(new_file, "w")
    writer = csv.writer(csvfile_w)
    idx = 0
    num = 0
    with open(old_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if idx == 0:
                writer.writerow(row)
                idx += 1
                continue
            dura = float(row[-3])
            dis = float(row[-2])
            speed = float(row[-1])
            # if dura <= 900:
            #     num += 1
            # if dis != -1 and dis <= 4000:
            #     num += 1
            # if speed != '-1' and speed <= 2.78:
            #     num += 1
            if dura <= 600 and (dis != -1 and dis <= 2000):
                num += 1
                writer.writerow(row)

    csvfile_w.close()
    print(num)

# add distance and speed
compute_dis_speed('data/NYC_taxi/train.csv', 'data/NYC_taxi/train_add.csv')

# filter duration, distance, speed
filter_dura_dis_speed('data/NYC_taxi/train_add.csv', 'data/NYC_taxi/train_filter.csv')