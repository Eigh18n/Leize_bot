from nonebot import *
import json
from random import randint
import requests,random,os,json,re
from hoshino import Service,R,priv,util
from hoshino.typing import MessageSegment,CQEvent, HoshinoBot
from hoshino.util import FreqLimiter,pic2b64
import hoshino
import asyncio
import time
import string
import random
import hashlib
import requests
import os
from  PIL  import   Image,ImageFont,ImageDraw
from io import BytesIO
import base64
from PIL import Image

#源码来源于https://github.com/Womsxd/YuanShen_User_Info
sv = Service('ysInfo', visible=True, manage_priv=priv.ADMIN, enable_on_default=True)
bot = get_bot()
mhyVersion = "2.7.0"


FILE_PATH = os.path.dirname(__file__)

class ImgText:
    FONTS_PATH = os.path.join(FILE_PATH,'fonts')
    FONTS = os.path.join(FONTS_PATH,'msyh1.otf')
    font = ImageFont.truetype(FONTS, 14)
    def __init__(self, text):
        # 预设宽度 可以修改成你需要的图片宽度
        self.width = 300
        # 文本
        self.text = text
        # 段落 , 行数, 行高
        self.duanluo, self.note_height, self.line_height, self.drow_height = self.split_text()
    def get_duanluo(self, text):
        txt = Image.new('RGBA', (400, 800), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 0
        for char in text:
            width, height = draw.textsize(char, ImgText.font)
            sum_width += width
            if sum_width > self.width: # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count
    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_duanluo(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        drow_height = total_lines * line_height
        return allText, total_height, line_height, drow_height
    def draw_text(self):
        """
        绘图以及文字
        :return:
        """
        im = Image.new("RGB", (300, self.drow_height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        # 左上角开始
        x, y = 0, 0
        for duanluo, line_count in self.duanluo:
            draw.text((x, y), duanluo, fill=(0, 0, 0), font=ImgText.font)
            y += self.line_height * line_count
        bio  = BytesIO()
        im.save(bio, format='PNG')
        base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
        mes  = f"[CQ:image,file={base64_str}]"
        return mes


def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return (md5.hexdigest())


def DSGet():
    global mhyVersion
    if (mhyVersion == "2.1.0"):
        n = md5(mhyVersion)
    else:
        mhyVersion = "2.7.0"
        n = "fd3ykrh7o1j54g581upo1tvpam0dsgtf"
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + n + "&t="+ i + "&r=" + r)
    return (i + "," + r + "," + c)

def GetInfo(Uid, ServerID):
    try:
        req = requests.get(
            url = "https://api-takumi.mihoyo.com/game_record/genshin/api/index?server="+ ServerID +"&role_id=" + Uid ,
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'DS': DSGet(),
                'Origin': 'https://webstatic.mihoyo.com',
                'Cookie': '',#自己获取
                'x-rpc-app_version': mhyVersion,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                'x-rpc-client_type': '2',
                'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'X-Requested-With': 'com.mihoyo.hyperion'
            }
        )
        return (req.text)
    except:
        print ("访问失败，请重试！")
        #sys.exit (1)
        return

def GetCharacter(Uid, ServerID, Character_ids):
    try:
        req = requests.post(
            url = "https://api-takumi.mihoyo.com/game_record/genshin/api/character",
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'DS': DSGet(),
                'Origin': 'https://webstatic.mihoyo.com',
                'Cookie': '',#自己获取
                'x-rpc-app_version': mhyVersion,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                'x-rpc-client_type': '2',
                'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'X-Requested-With': 'com.mihoyo.hyperion'
            },
            json = {"character_ids": Character_ids ,"role_id": Uid ,"server": ServerID }
        )
        return (req.text)
    except:
        print ("访问失败，请重试！")
        #sys.exit (1)
        return

def GetSpiralAbys(Uid, ServerID, Schedule_type):
    try:
        req = requests.get(
            url = "https://api-takumi.mihoyo.com/game_record/genshin/api/spiralAbyss?schedule_type=" + Schedule_type + "&server="+ ServerID +"&role_id=" + Uid,
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'DS': DSGet(),
                'Origin': 'https://webstatic.mihoyo.com',
                'Cookie': '',#自己获取                
                'x-rpc-app_version': mhyVersion,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                'x-rpc-client_type': '2',
                'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,en-US;q=0.8',
                'X-Requested-With': 'com.mihoyo.hyperion'
            }
        )
        return (req.text)
    except:
        print ("访问失败，请重试！")
        #sys.exit (1)
        return
        
def JsonAnalysis(JsonText,Uid, ServerID):
    data = json.loads(JsonText)
    if ( data["retcode"] != 0):
        return (
            "Api报错，返回内容为：\n" 
            + JsonText + "\n出现这种情况可能的UID输入错误 or 不存在"
        )
    else:
        pass
    Character_Info = "人物：\n"
    Character_List = []
    Character_List = data["data"]["avatars"]
    Character_ids = []
    for i in Character_List:
        Character_ids +=  [i["id"]]
    dataC = json.loads(GetCharacter(Uid, ServerID, Character_ids)) 
    Character_datas = dataC["data"]["avatars"]
    for i in Character_datas:
        Character_constellations = i["constellations"]
        weapon = i["weapon"]
        constellations = 0
        for j in Character_constellations:
            if (j["is_actived"] == 1):
                constellations += 1
        if (i["element"] == "None"):
            Character_Type = "无属性"
        elif (i["element"] == "Anemo"):
            Character_Type = "风属性"
        elif (i["element"] == "Pyro"):
            Character_Type = "火属性"
        elif (i["element"] == "Geo"):
            Character_Type = "岩属性"
        elif (i["element"] == "Electro"):
            Character_Type = "雷属性"
        elif (i["element"] == "Cryo"):
            Character_Type = "冰属性"
        elif (i["element"] == "Hydro"):
            Character_Type = "水属性"
        else:
            Character_Type = "草属性"
        if (i["name"] == "旅行者"):
            if (i["image"].find("UI_AvatarIcon_PlayerGirl") != -1):
                TempText = (
                    i["name"]+ "[萤——妹妹]" + 
                    "\n" + str(i["level"]) + "级，" 
                    + Character_Type 
                )
            elif (i["image"].find("UI_AvatarIcon_PlayerBoy") != -1):
                TempText = (
                    i["name"]+ "[空——哥哥]" + 
                    "\n" + str(i["level"]) + "级，" 
                    + Character_Type 
                )
            else:
                TempText = (
                    i["name"]+ "[性别判断失败]" + 
                    "\n" + str(i["level"]) + "级，" 
                    + Character_Type 
                )
        else:
            TempText = (
                str(i["name"])
                +"\n" + str(i["level"]) + "级，" 
                + "好感度为" + str(i["fetter"]) + "级，" 
                + str(constellations) + "命，"
                + str(i["rarity"]) + "★角色，"
                + Character_Type + "\n"
                + "武器 ：" + str(weapon["name"]) + " " + str(weapon["level"]) + "级 " + " 精炼" + str(weapon["affix_level"]) + "阶"
                + "\n"
            )
        Character_Info = Character_Info + TempText
    Account_Info = (
        "活跃天数：" + str(data["data"]["stats"]["active_day_number"]) +
        "天，\n共" + str(data["data"]["stats"]["achievement_number"]) +
        "个成就，\n风神瞳" + str(data["data"]["stats"]["anemoculus_number"]) +
        "个，\n岩神瞳" + str(data["data"]["stats"]["geoculus_number"]) +
        "个，\n获得了" + str(data["data"]["stats"]["avatar_number"]) +
        "个角色，\n解锁" + str(data["data"]["stats"]["way_point_number"]) +
        "个传送点和" + str(data["data"]["stats"]["domain_number"]) +
        "个秘境，\n深渊当期"
    )
    if (data["data"]["stats"]["spiral_abyss"] == "-"):
        Account_Info = Account_Info + "没打"
    else:
        Account_Info = Account_Info + "打到了" + data["data"]["stats"]["spiral_abyss"]
    Account_Info = Account_Info + (
        "\n宝箱：\n" + str(data["data"]["stats"]["common_chest_number"]) +
        "个普通，\n" + str(data["data"]["stats"]["exquisite_chest_number"]) +
        "个精致，\n" + str(data["data"]["stats"]["precious_chest_number"]) +
        "个珍贵，\n" + str(data["data"]["stats"]["luxurious_chest_number"]) +
        "个华丽"
    )
    Prestige_Info = "世界探索：\n"
    Prestige_list = []
    Prestige_list = data["data"]["world_explorations"]
    for i in Prestige_list:
        if i["type"] == "Offering":
            Prestige_Info = (Prestige_Info + i["name"] +
            "的探索为" + str(i["exploration_percentage"] / 10) +
            "%，供奉等级为：" + str(i["level"]) + "级\n")
        elif i["type"] == "Reputation":
             Prestige_Info = (Prestige_Info + i["name"] +
            "的探索为" + str(i["exploration_percentage"] / 10) +
            "%，声望等级为：" + str(i["level"]) + "级\n") 
    return (Character_Info + "\r\n" + Account_Info + "\r\n" + Prestige_Info)

def JsonSpiralAbys(JsonText,Schedule_type):
    data = json.loads(JsonText)
    if ( data["retcode"] != 0):
        return (
            "Api报错，返回内容为：\n" 
            + JsonText + "\n出现这种情况可能的UID输入错误 or 不存在"
        )
    else:
        pass
    TemptTex = ""
    if (data["data"]["max_floor"] == "0-0"):
        if Schedule_type == "1":
            SpiralAbys_Info = "没有进行本期深境螺旋\n"
        elif Schedule_type == "2":
            SpiralAbys_Info = "没有进行上期深境螺旋\n"
    else:
        if Schedule_type == "1":
            SpiralAbys_Info = "本期深境螺旋：\n"
        elif Schedule_type == "2":
            SpiralAbys_Info = "上期深境螺旋：\n"
        SpiralAbys_Info += (
            "最深抵达：" + str(data["data"]["max_floor"]) +
            "  战斗次数：" + str(data["data"]["total_battle_times"]) +
            "  总星数：" + str(data["data"]["total_star"]) + "\n"
        )
        SpiralAbys_List = []
        SpiralAbys_List = data["data"]["floors"]
        
        for i in SpiralAbys_List:
            SpiralAbys_Info = SpiralAbys_Info + (
                "第" + str(i["index"]) + "层" + 
                 "     星数:" + str(i["star"]) + "/" + str(i["max_star"])+ "\n"
            )
            for j in i["levels"]:
                SpiralAbys_Info = SpiralAbys_Info + (
                    "第" + str(j["index"]) + "间：" +
                    str(j["star"]) + "星         " 
                )
            SpiralAbys_Info = SpiralAbys_Info + "\n"
    return ( SpiralAbys_Info )


    
@sv.on_prefix('原神信息')
async def genshin(bot, ev: CQEvent):
    uid = ev.message.extract_plain_text()
    if not re.fullmatch('[0-9]*', uid):
        await bot.send(ev, uid, at_sender=True)
        return
    uid = uid.lstrip('0')
    if not uid:
        await bot.send(ev, '请输入原神信息uid（仅支持国服） 如：原神信息100692770', at_sender=True)
        sv.logger.info('原神uid不对')
        return
    if (len(uid) == 9):
        if (uid[0] == "1"):
            sv.logger.info('原神查询uid中')
            await bot.send(ev,'原神查询uid中')
            UidInfo = JsonAnalysis(GetInfo(uid ,"cn_gf01"),uid ,"cn_gf01")
            sv.logger.info('原神uid查询成功')
            tas_list = []
            msg_text = f'UID{uid} (官服)的信息为：\r\n{UidInfo}'
            n = ImgText(msg_text)
            mes = n.draw_text()
            data = {
                "type": "node",
                "data": {
                    "name": "imhy",
                    "uin": "2093936907",
                    "content":mes
                        }
                    }
            tas_list.append(data)
            await bot.send(ev, mes, at_sender=True)
            #await bot.send_group_forward_msg(group_id=ev['group_id'], messages=tas_list)
        elif (uid[0] == "5"):
            sv.logger.info('原神查询uid中')
            UidInfo = JsonAnalysis(GetInfo(uid ,"cn_gf01"),uid ,"cn_gf01")
            sv.logger.info('原神uid查询成功')
            tes_list = []
            msg_text = f'UID{uid} (官服)的信息为：\r\n{UidInfo}'
            n = ImgText(msg_text)
            mes = n.draw_text()
            data = {
                "type": "node",
                "data": {
                    "name": "imhy",
                    "uin": "2093936907",
                    "content":mes
                        }
                    }
            tes_list.append(data)
            await bot.send(ev, mes, at_sender=True)
            #await bot.send_group_forward_msg(group_id=ev['group_id'], messages=tes_list)
        else:
            sv.logger.info('原神uid不对')
            await bot.send(ev, 'UID输入有误！\n请检查UID是否为国服UID！', at_sender=True)
    else:
        sv.logger.info('原神uid不对')
        await bot.send(ev, 'UID长度有误！\n请检查输入的UID是否为9位数！', at_sender=True)

@sv.on_prefix('原神深渊')
async def genshin(bot: HoshinoBot, ev: CQEvent):
    args = ev.message.extract_plain_text().split()
    if len(args) == 1:
        uid = ev.message.extract_plain_text()
        Schedule_type = "1"
    elif len(args) ==2:
        uid = args[1]
        if args[0] == '本期':
            Schedule_type = "1"
        elif args[0] == '上期':
            Schedule_type = "2"
        else:
            await bot.finish(ev,'请重新输入', at_sender=True)
    else:
        await bot.finish(ev,'请重新输入', at_sender=True)
    if not re.fullmatch('[0-9]*', uid):
        await bot.send(ev, uid, at_sender=True)
        return
    uid = uid.lstrip('0')
    if not uid:
        await bot.send(ev, '请输入 原神深渊+（本期或上期）+uid （注：不加默认本期） \n如：原神深渊 100692770', at_sender=True)
        sv.logger.info('原神uid不对')
        return
    if (len(uid) == 9):
        if (uid[0] == "1"):
            sv.logger.info('原神深渊查询中')
            await bot.send(ev,'原神深渊查询中')
            SpiralAbysInfo = JsonSpiralAbys(GetSpiralAbys(uid ,"cn_gf01" ,Schedule_type), Schedule_type)
            sv.logger.info('原神深渊查询成功')
            tas_list = []
            msg_text = f'UID{uid} (官服)的深渊信息为：\r\n{SpiralAbysInfo}'
            n = ImgText(msg_text)
            mes = n.draw_text()
            data = {
                "type": "node",
                "data": {
                    "name": "imhy",
                    "uin": "2093936907",
                    "content":mes
                        }
                    }
            tas_list.append(data)
            await bot.send(ev, mes, at_sender=True)
            #await bot.send_group_forward_msg(group_id=ev['group_id'], messages=tas_list)
        elif (uid[0] == "5"):
            sv.logger.info('原神深渊查询中')
            SpiralAbysInfo = JsonSpiralAbys(GetSpiralAbys(uid ,"cn_gf01"), Schedule_type)
            sv.logger.info('原神深渊查询成功')
            tes_list = []
            msg_text = f'UID{uid} (官服)的深渊信息为：\r\n{SpiralAbysInfo}'
            n = ImgText(msg_text)
            mes = n.draw_text()
            data = {
                "type": "node",
                "data": {
                    "name": "imhy",
                    "uin": "2093936907",
                    "content":mes
                        }
                    }
            tes_list.append(data)
            await bot.send(ev, mes, at_sender=True)
            #await bot.send_group_forward_msg(group_id=ev['group_id'], messages=tes_list)
        else:
            sv.logger.info('原神uid不对')
            await bot.send(ev, 'UID输入有误！\n请检查UID是否为国服UID！', at_sender=True)
    else:
        sv.logger.info('原神uid不对')
        await bot.send(ev, 'UID长度有误！\n请检查输入的UID是否为9位数！', at_sender=True)