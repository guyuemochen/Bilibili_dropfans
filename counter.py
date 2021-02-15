import requests
import json
import time


def get_info(uid):
    # 获取API的数据
    data = requests.get('https://api.bilibili.com/x/web-interface/card?mid=' + str(uid))
    # 将数据转为JSON格式
    info = json.loads(data.text)
    # 将获得的数据以json形式返回
    return info


def sum(list):
    # 统计列表中所有数据之和
    sumall = 0
    for i in range(len(list)):
        sumall += list[i]
    return sumall


if __name__ == "__main__":
    uid = 777536  # B站uid，此处以LexBurner为例
    last_fan = 0  # 上次统计的粉丝数据
    has_dropped = 0
    drop_time = []
    # 初始化数组，设定一个100位数组
    for i in range(0, 100):
        drop_time.append(0)
    # 设置初始指针
    pointer = 0

    # 立一个flag，其实没啥用
    timeused = 0

    while True:
        info = get_info(uid)

        # 获得up名称以及粉丝数量，并转换成对应类型
        fans = int(info['data']['card']['fans'])
        name = info['data']['card']['name']

        # 为初始数据进行设置
        if last_fan == 0:
            last_fan = int(fans)

        #获取这次计算后掉粉数量
        dropped = last_fan - fans

        # 设置刷新时间，以保证数据为最新的100份
        drop_time[pointer] = dropped
        # 设置指针
        if pointer == 99:
            pointer = 0
            timeused = 100
        else:
            pointer += 1
        has_dropped += dropped
        target = fans // 100000

        # 防止drop_time之和为0
        try:
            if timeused == 100:
                time_left = ((fans - target * 100000) // (sum(drop_time) / timeused / 10))  # 计算获得100份数据剩余掉粉时间
            else:
                time_left = ((fans - target * 100000) // (sum(drop_time) / pointer / 10))  # 计算获得小于100份数据时剩余的掉粉时间
        except Exception:
            time_left = 0

        output = str(time.strftime("%b %d %H:%M:%S", time.localtime())) + " | " + name + " | 当前粉丝数：" \
                 + str(fans) + " | 距上次后掉粉数量：" + str(dropped) + " | 总计已掉粉：" + str(has_dropped) \
                 + " | 预计掉粉至" + str(target) + "0w剩余时间："

        # 设置输出剩余时间形式以方便阅读
        if time_left < 60:
            output = output + str(time_left) + "s"
        elif time_left < 3600:
            output = output + str(int(time_left / 6) / 10) + "m"
        elif time_left < 86400:
            output = output + str(int(time_left / 360) / 10) + "h"
        else:
            output = output + str(int(time_left / 8640) / 10) + "d"

        # 输出
        print(output)
        # 将获得的粉丝数量设定为上次的
        last_fan = fans
        # 防止被墙，设定每10秒运行一次
        time.sleep(10)
