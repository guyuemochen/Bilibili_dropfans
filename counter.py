#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import requests
import time
from colorama import Fore, Back, Style, init

init(autoreset=True)


def get_info(uid):
    # 获取API的数据
    data = requests.get('https://api.bilibili.com/x/web-interface/card?mid=' + str(uid))
    # 将数据转为JSON格式
    info = json.loads(data.text)
    # 将获得的数据以json形式返回
    return info


if __name__ == "__main__":
    uid = 777536  # B站uid，此处以LexBurner为例
    last_fan = 0  # 上次统计的粉丝数据
    has_dropped = 0
    drop_time = {}
    keys = []
    # 初始设置数组长度为60
    storage = 60

    # 进行初次数据采集
    info = get_info(uid)
    # 获得up名称以及粉丝数量，并转换成对应类型
    fans = int(info['data']['card']['fans'])
    name = info['data']['card']['name']
    path = 'last_time_data.txt'
    try:
        file = open(path)
        read = file.read()
        if read is not None:
            list1 = read.split(' ')
            drop_time[float(list1[0])] = int(list1[1])
            last_fan = int(list1[1])
            has_dropped = int(list1[2])
        else:
            last_fan = int(fans)
        file.close()
    except Exception as e:
        print(e)
    file = open(path, mode='w')
    write = str(time.time()) + " " + str(fans) + " " + str(has_dropped + last_fan - fans)
    file.writelines(write)
    file.close()


    while True:
        info = get_info(uid)

        # 获得up名称以及粉丝数量，并转换成对应类型
        fans = int(info['data']['card']['fans'])
        name = info['data']['card']['name']

        # 获取这次计算后掉粉数量
        dropped = last_fan - fans

        has_dropped += dropped

        while len(drop_time) >= storage:
            keys = list(drop_time.keys())
            del drop_time[keys[0]]
        drop_time[time.time()] = int(fans)

        keys = list(drop_time.keys())

        target = fans // 100000

        # 防止drop_time之和为0
        try:
            time_left = (fans - target * 100000) // ((drop_time[keys[0]] - drop_time[keys[len(keys) - 1]]) / (keys[len(keys) - 1] - keys[0]))
        except Exception:
            time_left = 2592000

        if dropped >= 0:
            output = str(time.strftime("%b %d %H:%M:%S", time.localtime())) + " | " + name + " | 当前粉丝数：" \
                     + str(fans) + " | 粉丝减少：" + str(dropped) + " | 总计已掉粉：" + str(has_dropped) \
                     + " | 预计掉粉至" + str(target) + "0w剩余时间："
        else:
            output = str(time.strftime("%b %d %H:%M:%S", time.localtime())) + " | " + name + " | 当前粉丝数：" \
                     + str(fans) + " | 粉丝" + Fore.BLACK + Back.LIGHTYELLOW_EX + '增加' + Style.RESET_ALL + "：" \
                     + str(-dropped) + " | 总计已掉粉：" + str(has_dropped) + " | 预计掉粉至" + str(target) + "0w剩余时间："

        # 设置输出剩余时间形式以方便阅读
        # 动态调整数组长度以保证数据准确性
        if time_left < 60:
            output = output + str(time_left) + "s"
        elif time_left < 3600:
            # 剩余时间少于一小时时仅保存最后10个数据
            output = output + str(int(time_left / 6) / 10) + "m"
            storage = 10
        elif time_left < 86400:
            # 剩余时间小于一天时，仅保存60个数据
            output = output + str(int(time_left / 360) / 10) + "h"
            storage = 60
        elif time_left < 2592000:
            # 剩余时间大于一天时，保存3600个数据
            output = output + str(int(time_left / 8640) / 10) + "d"
            storage = 3600
        else:
            # 如果超过一个月（此处以30天计算）输出‘>1m’
            output = output + '>30d'

        # 输出
        print(output)

        output = ''
        for i in range(110):
            output = output + '-'
        print(output)
        # 将获得的粉丝数量设定为上次的
        last_fan = fans
        # 防止被墙，设定每10秒运行一次
        time.sleep(10)
