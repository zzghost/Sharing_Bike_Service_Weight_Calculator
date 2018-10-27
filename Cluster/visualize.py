#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file:visualize.py
@time:2018/07/20

Compute cluster centers based on pickup position for four time periods both in work days and weekend, and visualize the map
"""
# %matplotlib inline
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import json
from sklearn.cluster import KMeans
import time

time_interval = range(0,4)
time_num_cluster = [100 for i in range(0,4)]

rows_lon = []
rows_lat = []
rows_time = []
rows_dura = []
rows_dis = []
rows_speed = []
rows_person = []
rows_lon_lat = []
PICKUP = True
DROPOUT = False
ISWORK = True

# read the train_filter.csv
idx = 0
with open('data/NYC_taxi/train_filter.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if idx == 0:
            idx += 1
            continue
        # rows_dura.append(float(row[-3]))
        # if row[-2] != '-1':
        #     rows_dis.append(float(row[-2]))
        # if row[-1] != '-1':
        #     rows_speed.append(float(row[-1]))

        start_time = row[2]
        timeArray = time.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        dayofweek = time.strftime("%w", timeArray)
        # print(dayofweek)

        if ISWORK:
            if dayofweek == '0' or dayofweek == '6':
                continue
        else:
            if dayofweek != '0' and dayofweek != '6':
                continue

        if PICKUP:
            rows_lon.append(float(row[5]))
            rows_lat.append(float(row[6]))
            cmp_time = int(row[2].split()[1].split(':')[0])
            p_time = 0
            if cmp_time < 6:
                p_time = 0
            elif cmp_time >= 6 and cmp_time < 12:
                p_time = 1
            elif cmp_time >= 12 and cmp_time < 18:
                p_time = 2
            elif cmp_time >= 18 and cmp_time < 24:
                p_time = 3
            # rows_time.append(int(cmp_time))
            # rows_person.append(int(row[4]))
            rows_lon_lat.append([float(row[5]), float(row[6]), p_time, int(row[4])])
        if DROPOUT:
            rows_lon.append(float(row[7]))
            rows_lat.append(float(row[8]))
            cmp_time = int(row[3].split()[1].split(':')[0])
            p_time = 0
            if cmp_time < 6:
                p_time = 0
            elif cmp_time >= 6 and cmp_time < 12:
                p_time = 1
            elif cmp_time >= 12 and cmp_time < 18:
                p_time = 2
            elif cmp_time >= 18 and cmp_time < 24:
                p_time = 3
            # rows_time.append(int(cmp_time))
            # rows_person.append(int(row[4]))
            rows_lon_lat.append([float(row[7]), float(row[8]), p_time, int(row[4])])
print(len(rows_lon))
print(len(rows_lat))
# print(len(rows_time))
# print(len(rows_person))
print(len(rows_lon_lat))

# print('原始数据')
print(min(rows_lon), max(rows_lon))
print(min(rows_lat), max(rows_lat))
# print(min(rows_time), max(rows_time))
# print(min(rows_person), max(rows_person))
# print(min(rows_dura), max(rows_dura))
# print(min(rows_dis), max(rows_dis))
# print(min(rows_speed), max(rows_speed))
rows_lon = np.array(rows_lon)
rows_lat = np.array(rows_lat)
rows_lon_lat = np.array(rows_lon_lat)



def ana_data(mrcData):
    """
    Compute the average, std, minimum and maximum
    """
    if type(mrcData) is list:
        mrcData = np.array(mrcData)
    avg = mrcData.mean()
    stddev = np.std(mrcData, ddof=1)
    minval = mrcData.min()
    maxval = mrcData.max()
    print('avg:', avg)
    print('std:', stddev)
    print('min:', minval)
    print('max:', maxval)
    return avg, stddev, minval, maxval

def mapstd(data_lon, data_lat, data_lon_lat):
    # print('\n')
    # print('lon')
    # avg_lon, stddev_lon, minval_lon, maxval_lon = ana_data(data_lon)
    # print('lat')
    # avg_lat, stddev_lat, minval_lat, maxval_lat = ana_data(data_lat)
    # # avg = mrcData.mean()
    # # stddev = np.std(mrcData,ddof=1)
    # # minval = mrcData.min()
    # # maxval = mrcData.max()
    #
    # sigma_contrast = 0.5
    # # minval_lon = avg_lon - sigma_contrast * stddev_lon
    # # maxval_lon = avg_lon + sigma_contrast * stddev_lon
    # # minval_lat = avg_lat - sigma_contrast * stddev_lat
    # # maxval_lat = avg_lat + sigma_contrast * stddev_lat

    minval_lon = -74.05
    maxval_lon = -73.90
    minval_lat = 40.700
    maxval_lat = 40.850

    new_data = []
    for e_data in data_lon_lat:
        if e_data[0] > minval_lon and e_data[0] < maxval_lon and e_data[1] > minval_lat and e_data[1] < maxval_lat:
            new_data.append(e_data)
    new_data = np.array(new_data)

    print(min(new_data[:, 0]), max(new_data[:, 0]))
    print(min(new_data[:, 1]), max(new_data[:, 1]))
    print(len(new_data))

    # new_data_lon = new_data[:, 0]
    # new_data_lat = new_data[:, 1]
    return new_data


def get_time_data(data):
    """
    Get data for four time periods
    """
    global time_interval
    # cur_t = 0
    new_data = []
    for i_time in time_interval:
        cur_idx = np.where(data[:, 2] == i_time)
        cur_data = data[cur_idx[0]]
        # print(str(i_time) + ' ', len(cur_data))
        # cur_t += len(cur_data)
        new_data.append(cur_data)
    new_data = np.array(new_data)
    # print(cur_t)

    return new_data


def plot(draw_x, draw_y, draw_label, cen_x, cen_y, cen_num_car, v_time, has_centers=False):
    plt.figure()
    plt.cla()
    plt.axis([min(draw_x), max(draw_x), min(draw_y), max(draw_y)])

    # plt.scatter(draw_x, draw_y, marker='o', color='r', s=0.1, label=str(v_time))
    plt.scatter(draw_x, draw_y, marker='o', c=draw_label, cmap=plt.cm.Reds, alpha=0.5, s=0.1, label=str(v_time))
    if has_centers:
        bar = plt.scatter(cen_x, cen_y, marker='o', c=cen_num_car, cmap=plt.cm.Greens, s=10, label='centers')
        plt.colorbar(bar)

    plt.legend(loc='best')  # 设置 图例所在的位置 使用推荐位置
    plt.xlabel('longitude')  # 给 x 轴添加标签
    plt.ylabel('latitude')  # 给 y 轴添加标签
    plt.title('The figure of taxis in this time period in working days')  # 添加图形标题
    plt.show()
    # plt.savefig('data/pickup_time/pickup_%d.png' % v_time)
    # print('data/pickup_time/pickup_%d.png' % v_time + 'done.')


# analyze data
# print('lon')
# ana_data(rows_lon)
# print('lat')
# ana_data(rows_lat)
# print('duration')
# ana_data(rows_dura)
# print('distance')
# ana_data(rows_dis)
# print('speed')
# ana_data(rows_speed)


# generate result
result_dic = {}
# plot(rows_lon_lat[:,0], rows_lon_lat[:,1], rows_lon_lat, rows_lon_lat, 0, has_centers=False)
new_lon_lat = mapstd(rows_lon, rows_lat, rows_lon_lat)
# plot(new_lon_lat[:,0], new_lon_lat[:,1], rows_lon_lat, rows_lon_lat, 0, has_centers=False)
new_time_lon_lat = get_time_data(new_lon_lat)

for i_time in time_interval:
    result_list_2 = []
    result_list = np.zeros((time_num_cluster[i_time], 4), dtype=np.float)
    # if i_time > 1: break
    cur_lon = new_time_lon_lat[i_time][:, 0]
    cur_lat = new_time_lon_lat[i_time][:, 1]
    cur_lon_lat = new_time_lon_lat[i_time][:, 0:2]
    cur_person = new_time_lon_lat[i_time][:, 3]
    # kmeans
    t1 = time.time()
    kmeans = KMeans(n_clusters=time_num_cluster[i_time], random_state=0).fit(cur_lon_lat)
    print(time.time() - t1)
    label_array = kmeans.labels_
    res_centers = kmeans.cluster_centers_
    nrof_centers = len(res_centers)
    ct_count = np.zeros((nrof_centers), dtype=np.int32)
    ct_person_count = np.zeros((nrof_centers), dtype=np.int32)
    for label_id in range(nrof_centers):
        cur_emb_idx = np.where(label_array == label_id)
        ct_count[label_id] = len(cur_emb_idx[0])
        cur_emb_person = cur_person[cur_emb_idx[0]]
        ct_person_count[label_id] = np.sum(cur_emb_person)

    result_list[:, 0:2] = res_centers
    result_list[:, 2] = ct_count
    result_list[:, 3] = ct_person_count
    for i in range(len(result_list)):
        result_list_2.append(list(result_list[i]))
    result_dic[str(i_time)] = result_list_2

    cen_lon = res_centers[:, 0]
    cen_lat = res_centers[:, 1]

    cur_label = label_array
    cen_num_car = ct_count
    cen_num_person = ct_person_count

    plot(cur_lon, cur_lat, cur_label, cen_lon, cen_lat, cen_num_car+cen_num_person, i_time, has_centers=True)
# plt.show()

# print(result_dic)
with open("data/NYC_taxi/result_centers_workday.json","w") as f:
     json.dump(result_dic,f)










