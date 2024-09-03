import asyncio
import os
import sys
import decimal
import random

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


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

def mai_rating(grading, acc):
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