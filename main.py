import asyncio
import os
import sys
import decimal
import random
from variable import alias_url, song_name_url
import requests
import json

sys.path.append('./src/libraries/')

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message
from maimaib50 import generate50 # type: ignore

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

maimai_list = ['拼机', '推分', '越级', '夜勤', '练底力', '练手法', '干饭', '抓绝赞', '收歌']

def download(url1, url2):
    done1 = 1
    alias_file_temp = requests.get(url1)
    # if alias_file_temp.status_code == 200:
    #     done1 = 1
    # else:
    #     done1 = alias_file_temp.status_code
    if done1 == 1:
        with open('alias.json', 'w') as file1:
            json.dump(alias_file_temp.text, file1)

    done2 = 1
    song_name_file_temp = requests.get(url2).json()
    # if song_name_file_temp.status_code == 200:
    #     done2 = 1
    # else:
    #     done2 = song_name_file_temp.status_code
    if done2 == 1:
        with open('sn.json', 'w') as file2:
            json.dump(song_name_file_temp, file2)
    return done1

#计算单曲rating的函数
def mai_rating(grading, acc):
    #判断Rating因子
    def score_multiplier(acc):
        score = 0
        match acc:
            case(acc) if acc - 100.5 >= 0:
                score = 0.244
                #SSS+
            case(acc) if acc - 100.4999 >= 0 > acc - 100.5:
                score = 0.222
                #SSS
            case(acc) if acc - 100 >= 0 > acc - 100.4999:
                score = 0.216
                #SSS
            case(acc) if acc - 99.9999 >= 0 > acc - 100:
                score = 0.214
                #SS+
            case(acc) if acc - 99.5 >= 0 > acc - 100:
                score = 0.211
                #SS+
            case(acc) if acc - 99 >= 0 > acc - 99.5:
                score = 0.208
                #SS
            case(acc) if acc - 98.9999 >= 0 > acc - 99:
                score = 0.206
                #S+
            case(acc) if acc - 98 >= 0 > acc - 98.9999:
                score = 0.203
                #S+
            case(acc) if acc - 97 >= 0 > acc - 98:
                score = 0.2
                #S
            case(acc) if acc - 96.9999 >= 0 > acc - 97:
                score = 0.176
                #AAA
            case(acc) if acc - 94 >= 0 > acc - 96.9999:
                score = 0.168
                #AAA
            case(acc) if acc - 90 >= 0 > acc - 94:
                score = 0.152
                #AA
            case(acc) if acc - 80 >= 0 > acc - 90:
                score = 0.136
                #A
            case(acc) if acc - 79.9999 >= 0 > acc - 80:
                score = 0.128
                #BBB
            case(acc) if acc - 75 >= 0 > acc - 79.9999:
                score = 0.120
                #BBB
            case(acc) if acc - 70 >= 0 > acc - 75:
                score = 0.112
                #BB
            case(acc) if acc - 60 >= 0 > acc - 70:
                score = 0.096
                #B
            case(acc) if acc - 50 >= 0 > acc - 60:
                score = 0.08
                #C
            case(acc) if acc - 40 >= 0 > acc - 50:
                score = 0.064
                #D
            case(acc) if acc - 30 >= 0 > acc - 40:
                score = 0.048
                #D
            case(acc) if acc - 20 >= 0 > acc - 30:
                score = 0.032
                #D
            case(acc) if acc - 10 >= 0 > acc - 20:
                score = 0.016
                #D

        return score
    decimal_acc = decimal.Decimal(acc)
    multiplier = decimal.Decimal(score_multiplier(acc))
    rating = grading * decimal_acc * multiplier
    new_rating = int(rating)
    return new_rating


class MyClient(botpy.Client):
    #在Bot准备好后输出一条消息
    async def on_ready(self):
        _log.info(f"「{self.robot.name}」准备好了喵~")

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        #让频道主可以远程关闭程序
        if "下线" in message.content:
            if "Neko" in message.author.username:
                await message.reply(content="下班喵~")
                sys.exit(0)
            else:
                await message.reply(content="你谁喵~")
        #计算单曲rating
        if "/rating" in message.content:
            str1 = message.content
            str2 = str1.split()
            grading = decimal.Decimal(str2[2])
            acc = float(str2[3])
            rating = mai_rating(grading, acc)
            await message.reply(content=f"此曲Rating是 {rating}")
            await message.reply(content="喵~")
            print(f"Rating:{rating}")
        #给出随机建议
        if "/今日份的舞萌" in message.content:
            temp_random = random.randint(1, 6)
            match temp_random:
                case (temp_random) if temp_random == 1:
                    await message.reply(content="拼个机喵~")
                case (temp_random) if temp_random == 2:
                    await message.reply(content="去推分喵~")
                case (temp_random) if temp_random == 3:
                    await message.reply(content="越个级喵~")
                case (temp_random) if temp_random == 4:
                    await message.reply(content="晚上出勤喵~")
                case (temp_random) if temp_random == 5:
                    await message.reply(content="练一练喵~")
                case (temp_random) if temp_random == 6:
                    await message.reply(content="吃饭去喵~")
            print(f"今日份：{temp_random}")
        #给出 宜/忌
        if "/舞萌运势" in message.content:
            temp_1 = random.randint(1, 3)
            temp_2 = random.randint(1, 3)
            list_1 = []
            list_2 = []
            for a in range(1, (temp_1 + 1)):
                list_1.append(maimai_list[random.randint(0, len(maimai_list)) - 1])
            for b in range(1, (temp_2 + 1)):
                list_2.append(maimai_list[random.randint(0, len(maimai_list)) - 1])
            list_1 = list(set(list_1))
            list_2 = list(set(list_2))
            temp_str_1 = "宜：" + f"{list_1[0]} "
            for c in range(1, len(list_1)):
                temp_str_1 = temp_str_1 + f"{list_1[(c)]} "
            await message.reply(content=f"{temp_str_1}")
            temp_str_2 = "忌：" + f"{list_2[0]} "
            for d in range(1, len(list_2)):
                temp_str_2 = temp_str_2 + f"{list_2[(d)]} "
            await message.reply(content=f"{temp_str_2}")
            await message.reply(content="喵~")
        #从水鱼查分器拿到b50并绘制成图
        if "/b50" in message.content:
            payload ={}
            str3 = message.content
            str4 = str3.split()
            payload['username'] = f"{str4[2]}"
            payload['b50'] = "True"
            print(payload)
            await generate50(payload)
            await message.reply(content=f"", file_image="./1.png")
            await message.reply(content="b50来了喵~")
            bool_1 = os.path.isfile("./1.png")
            if bool_1:
                await os.remove("./1.png")
        #给出一个有概率的0-100的幸运值
        if "/lucky" in message.content:
            luck_temp_1 = random.randint(1, 100)
            match luck_temp_1:
                case (luck_temp_1) if luck_temp_1 < 30:
                    luck_1 = random.randint(0,40)
                case (luck_temp_1) if 30 <= luck_temp_1 < 70:
                    luck_1 = random.randint(41, 70)
                case (luck_temp_1) if 70 <= luck_temp_1 < 95:
                    luck_1 = random.randint(71, 90)
                case (luck_temp_1) if luck_temp_1 >= 95:
                    luck_1 = random.randint(91, 100)
            await message.reply(content=f"你的幸运值 {luck_1} 喵~")
            match luck_1:
                case (luck_1) if luck_1 >= 85:
                    await message.reply(content=f"运气很好喵~")
                case (luck_1) if 60 <= luck_1 < 85:
                    await message.reply(content=f"运气不错喵~")
                case (luck_1) if 40 < luck_1 <= 60:
                    await message.reply(content=f"运气不是很好喵~")
                case (luck_1) if 0 < luck_1 <= 40:
                    await message.reply(content=f"要不今天休息一天喵~")
        #帮助
        if "/help" in message.content:
            await message.reply(content="/rating <定级> <达成率>\n/今日份的舞萌\n/舞萌运势\n/b50 <水鱼账号>\n/lucky\n/查歌 <1/2> <别名/乐曲id>")
        sn_data = []
        with open('alias.json', 'r') as file1:
            a_data = json.loads(json.load(file1))
        # with open('sn.json', 'r') as file2:
        #     sn_data = file2
        #     sn_data = file2
        # sn_data = os.open('sn.json', os.O_RDONLY)
        with open('sn.json', 'r') as  file2:
            sn_data = json.load(file2)
        reverse_dict = {}
        for key, value_list in a_data.items():
            for value in value_list:
                if value in reverse_dict:
                    # 如果值已经在反向字典中，添加当前键到该值的键列表中
                    reverse_dict[value].append(key)
                else:
                    # 如果值不在反向字典中，为该值创建一个新的键列表并添加当前键
                    reverse_dict[value] = [key]
        if "/获取别名库" in message.content:
            if "Neko" in message.author.username:
                # code = download(alias_url, song_name_url)
                download(alias_url, song_name_url)
                # await message.reply(content="\n已向Xray服务器获取别名库")
                # if code == 1:
                #     await message.reply(content="\n已成功与Xray进行通信")
                # else:
                #     await message.reply(content=f"code:{code}")
                await message.reply(content=f"目前数据库有{len(a_data)}首乐曲")
        if "/查歌" in message.content:
            str1 = message.content
            str2 = str1.split()
            i_1 = int(str2[2])
            print(str2[3])
            print(i_1)
            if i_1 == 1:
                s_1 = reverse_dict[f"{str2[3]}"]
                print(s_1)
                for dict in sn_data:
                    if dict["id"] == s_1[0]:
                        title = dict['title']
                        print(title)
                        await message.reply(content=f"{title}")
                # await message.reply(content=f"{sn_data[]['title']}")
            else:
                await message.reply(content=f"{a_data[str2[3]]}")
        #输出触发Bot的话
        _log.info(message.content)
        #输出触发Bot者名称
        _log.info(message.author.username)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])