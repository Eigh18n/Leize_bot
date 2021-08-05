from nonebot import *
import json
from random import randint
import requests,random,os,json,re
from hoshino import Service,R,priv,util
from hoshino.typing import MessageSegment,CQEvent, HoshinoBot
from hoshino.util import FreqLimiter,pic2b64
from urllib.request import urlopen
import hoshino
import asyncio
import time
import urllib
import string
import random
import hashlib
import math
import requests
import os
from  PIL  import   Image,ImageFont,ImageDraw
from io import BytesIO
import io
import base64
from PIL import Image


#源码来源于https://github.com/Womsxd/YuanShen_User_Info
sv = Service('ysInfo', visible=True, manage_priv=priv.ADMIN, enable_on_default=True)
bot = get_bot()

mhyVersion = "2.9.0"
salt = "w5k9n3aqhoaovgw25l373ee18nsazydo" # Github-@Azure99
client_type = "5"
cache_Cookie = "" #自行获取

FILE_PATH = os.path.dirname(__file__)
FONTS_PATH = os.path.join(FILE_PATH,'fonts')
FONTS = os.path.join(FONTS_PATH,'sakura.ttf')
font = ImageFont.truetype(FONTS, 16)

def get_duanluo(text):
    txt = Image.new('RGBA', (600, 800), (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    # 所有文字的段落
    duanluo = ""
    max_width = 600
    # 宽度总和
    sum_width = 0
    # 几行
    line_count = 1
    # 行高
    line_height = 0
    for char in text:
        width, height = draw.textsize(char, font)
        sum_width += width
        if sum_width > max_width: # 超过预设宽度就修改段落 以及当前行数
            line_count += 1
            sum_width = 0
            duanluo += '\n'
        duanluo += char
        line_height = max(height, line_height)
    if not duanluo.endswith('\n'):
        duanluo += '\n'
    return duanluo, line_height, line_count

def split_text(content):
    # 按规定宽度分组
    max_line_height, total_lines = 0, 0
    allText = []
    for text in content.split('\n'):
        duanluo, line_height, line_count = get_duanluo(text)
        max_line_height = max(line_height, max_line_height)
        total_lines += line_count
        allText.append((duanluo, line_count))
    line_height = max_line_height
    total_height = total_lines * line_height
    drow_height = total_lines * line_height
    return allText, total_height, line_height, drow_height

def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def DSGet():
    n = salt
    i = str(int(time.time()))
    r = ''.join(random.sample(string.ascii_lowercase + string.digits, 6))
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return i + "," + r + "," + c



def GetInfo(Uid, ServerID):
    req = requests.get(
        url="https://api-takumi.mihoyo.com/game_record/genshin/api/index?server=" + ServerID + "&role_id=" + Uid,
        headers={
            'Accept': 'application/json, text/plain, */*',
            'DS': DSGet(),
            'Origin': 'https://webstatic.mihoyo.com',
            'x-rpc-app_version': mhyVersion,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
            'x-rpc-client_type': client_type,
            'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.mihoyo.hyperion',
            "Cookie": cache_Cookie
        }
    )
    return req.text

def GetCharacter(Uid, ServerID, Character_ids):
    try:
        req = requests.post(
            url = "https://api-takumi.mihoyo.com/game_record/genshin/api/character",
            headers = {
                'Accept': 'application/json, text/plain, */*',
                'DS': DSGet(),
                'Origin': 'https://webstatic.mihoyo.com',
                "Cookie": cache_Cookie,#自己获取
                'x-rpc-app_version': mhyVersion,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                'x-rpc-client_type': client_type,
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
                "Cookie": cache_Cookie,#自己获取
                'x-rpc-app_version': mhyVersion,
                'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
                'x-rpc-client_type': client_type,
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

def calcStringLength(text):
    # 令len(str(string).encode()) = m, len(str(string)) = n
    # 字符串所占位置长度 = (m + n) / 2
    # 但由于'·'属于一个符号而非中文字符所以需要把长度 - 1
    if re.search('·', text) is not None:
        stringlength = int(((str(text).encode()) + len(str(text)) - 1) / 2)
    elif re.search(r'[“”]', text) is not None:
        stringlength = int((len(str(text).encode()) + len(str(text))) / 2) - 2
    else:
        stringlength = int((len(str(text).encode()) + len(text)) / 2)

    return stringlength


def spaceWrap(text, flex=10):
    stringlength = calcStringLength(text)

    return '%s' % (str(text)) + '%s' % (' ' * int((int(flex) - stringlength)))


def elementDict(text, isOculus=False):
    elementProperty = str(re.sub(r'culus_number$', '', text)).lower()
    elementMastery = {
        "anemo": "风",
        "pyro": "火",
        "geo": "岩",
        "electro": "雷",
        "cryo": "冰",
        "hydro": "水",
        "dendro": "草",  # https://genshin-impact.fandom.com/wiki/Dendro
        "none": "无",
    }
    try:
        elementProperty = str(elementMastery[elementProperty])
    except KeyError:
        elementProperty = "草"
    if isOculus:
        return elementProperty + "神瞳"
    elif not isOculus:
        return elementProperty + "属性"




def JsonAnalysis(JsonText,Uid, ServerID):
    data = json.loads(JsonText)
    if data["retcode"] != 0:
        if data["retcode"] == 10001:
            os.remove("cookie.txt")
            return "Cookie错误/过期，请重置Cookie"
        return (
                "Api报错，返回内容为：\r\n"
                + JsonText + "\r\n出现这种情况可能是UID输入错误 or 不存在"
        )
    else:
        pass
    msg_list = []
    Character_Info = f'UID{Uid} 的信息为：\n'
    Character_Info += "人物：\n"
    msg_list.append(Character_Info)
    name_length = []
    Character_List = data["data"]["avatars"]
    Character_ids = []
    for i in Character_List:
        Character_ids +=  [i["id"]]
        name_length.append(calcStringLength(i["name"]))
    dataC = json.loads(GetCharacter(Uid, ServerID, Character_ids)) 
    Character_datas = dataC["data"]["avatars"]
    namelength_max = int(max(name_length))
    for i in Character_datas:
        weapon = i["weapon"]
        Character_Type = elementDict(i["element"], isOculus=False)
        if i["name"] == "旅行者":
            if i["image"].find("UI_AvatarIcon_PlayerGirl") != -1:
                msg_list.append('荧,'+str(i['icon']))
                msg_list.append(str(weapon['name'])+','+str(weapon['icon']))
                TempText = (
                        spaceWrap(str("荧"), namelength_max) +
                        "（" + spaceWrap(str(i["level"]), 2) + "级）"
                        + "武器 ：" + str(weapon["name"]) + " " + str(weapon["level"]) + "级 " + " 精炼" + str(weapon["affix_level"])
                )
                msg_list.append(TempText)
            elif i["image"].find("UI_AvatarIcon_PlayerBoy") != -1:
                msg_list.append('空,'+str(i['icon']))
                msg_list.append(str(weapon['name'])+','+str(weapon['icon']))
                TempText = (
                        spaceWrap(str("空"), namelength_max) +
                        "（" + spaceWrap(str(i["level"]), 2) + "级）"
                        + "武器 ：" + str(weapon["name"]) + " " + str(weapon["level"]) + "级 " + " 精炼" + str(weapon["affix_level"])
                )
                msg_list.append(TempText)

            else:
                msg_list.append('旅行者,'+str(i['icon']))
                msg_list.append(str(weapon['name'])+','+str(weapon['icon']))
                TempText = (
                        i["name"] + "[?]" +
                        "（" + spaceWrap(str(i["level"]), 2) + "级）"
                        + "武器 ：" + str(weapon["name"]) + " " + str(weapon["level"]) + "级 " + " 精炼" + str(weapon["affix_level"])
                )
                msg_list.append(TempText)

        else:
            msg_list.append(str(i["name"])+','+str(i['icon']))
            msg_list.append(str(weapon['name'])+','+str(weapon['icon']))
            TempText = (
                    spaceWrap(str(i["name"]), namelength_max) +
                    "（" + spaceWrap(str(i["level"]), 2) + "级，"
                    + str(i["actived_constellation_num"]) + "命）"
                     + "武器 ：" + str(weapon["name"]) + " " + str(weapon["level"]) + "级 " + " 精炼" + str(weapon["affix_level"])
            )
            msg_list.append(TempText)
        Character_Info = Character_Info + TempText
    Account_Info = "\n账号信息：\n"
    Account_Info += "活跃天数：　　" + str(data["data"]["stats"]["active_day_number"]) + "\n"
    Account_Info += "达成成就数量：" + str(data["data"]["stats"]["achievement_number"]) + "个\n"
    for key in data["data"]["stats"]:
        if re.search(r'culus_number$', key) is not None:
            Account_Info = "{}{}已收集：{}个\n".format(
                Account_Info,
                elementDict(str(key), isOculus=True),  # 判断神瞳属性
                str(data["data"]["stats"][key])
            )
        else:
            pass
    Account_Info += "获得角色数量：" + str(data["data"]["stats"]["avatar_number"]) + "个\n"
    Account_Info += "传送点已解锁：" + str(data["data"]["stats"]["way_point_number"]) + "个\n"
    Account_Info += "秘境解锁数量：" + str(data["data"]["stats"]["domain_number"]) + "个\n"
    Account_Info += "深渊当期进度："
    if data["data"]["stats"]["spiral_abyss"] != "-":
        Account_Info += data["data"]["stats"]["spiral_abyss"] + "\n"
    else:
        Account_Info += "没打\n"
    Account_Info = Account_Info + (
            "\n开启宝箱计数：\n" +
            "普通宝箱：" + str(data["data"]["stats"]["common_chest_number"]) + "个\n" +
            "精致宝箱：" + str(data["data"]["stats"]["exquisite_chest_number"]) + "个\n" +
            "珍贵宝箱：" + str(data["data"]["stats"]["precious_chest_number"]) + "个\n" +
            "华丽宝箱：" + str(data["data"]["stats"]["luxurious_chest_number"]) + "个\n"
    )
    msg_list.append(Account_Info)
    Area_list = data["data"]["world_explorations"]
    Prestige_Info = "区域信息：\n"
    ExtraArea_Info = "供奉信息：\n"

    # 排版开始
    prestige_info_length = []
    extra_area_info_length = []
    for i in Area_list:
        prestige_info_length.append(calcStringLength(i["name"] + " "))
        if len(i["offerings"]) != 0:
            extra_area_info_length.append(calcStringLength(str(i["offerings"][0]["name"]) + " "))

    prestige_info_length_max = max(prestige_info_length)
    extra_area_info_length_max = max(extra_area_info_length)
    # 排版结束

    for i in Area_list:
        if (i["type"] == "Reputation"):
            Prestige_Info = "{}\t{}探索进度：{}%，声望等级：{}级\n".format(
                Prestige_Info,
                spaceWrap(i["name"] + " ", prestige_info_length_max),  # 以最长的地名为准，自动补足空格
                spaceWrap(str(i["exploration_percentage"] / 10).replace("100.0", "100"), 4),  # 以xx.x%长度为准，自动补足空格
                spaceWrap(str(i["level"]), 2)
            )
        else:
            Prestige_Info = "{}\t{}探索进度：{}%\n".format(
                Prestige_Info,
                spaceWrap(i["name"] + " ", prestige_info_length_max),  # 以最长的地名为准，自动补足空格
                spaceWrap(str(i["exploration_percentage"] / 10).replace("100.0", "100"), 4)  # 以xx.x%长度为准，自动补足空格
            )
        if len(i["offerings"]) != 0:
            ExtraArea_Info = "{}\t{}供奉等级：{}级，位置：{}\n".format(
                ExtraArea_Info,
                spaceWrap(str(i["offerings"][0]["name"] + " "), extra_area_info_length_max),
                spaceWrap(str(i["offerings"][0]["level"]), 2),
                str(i["name"])
            )
    Home_Info = "家园信息：\n" + spaceWrap("已开启区域：", 16)
    Home_List = data["data"]["homes"]
    homeworld_list = []
    for i in Home_List:
        homeworld_list.append(i["name"])
    Home_Info += '、'.join(homeworld_list) + "\n"
    Home_Info += spaceWrap("最高洞天仙力：", 16) + str(Home_List[0]["comfort_num"]) + '（' + Home_List[0][
        "comfort_level_name"] + '）\n'
    Home_Info += "已获得摆件数量：" + str(Home_List[0]["item_num"]) + "\n"
    Home_Info += spaceWrap("最大信任等级：", 16) + str(Home_List[0]["level"]) + '级' + "\n"
    Home_Info += "最高历史访客数：" + str(Home_List[0]["visit_num"])
    msg_list.append(Prestige_Info)
    msg_list.append(ExtraArea_Info)
    msg_list.append(Home_Info)
    drow_height = 0
    shul = 1
    for msg in msg_list:
        #print('段落：' + str(msg))
        if 'jpg' in str(msg) or 'png' in str(msg):
            if shul%2 == 0:
                drow_height += 80
            shul += 1
        else:
            x_drow_duanluo, x_drow_note_height, x_drow_line_height, x_drow_height = split_text(msg)
            drow_height += x_drow_height
    
    base_img1 = os.path.join(FILE_PATH, "dt1.jpg")
    dtimg1 = Image.open(base_img1)
    
    base_img2 = os.path.join(FILE_PATH, "dt2.jpg")
    dtimg2 = Image.open(base_img2)
    
    base_img = os.path.join(FILE_PATH, "dt.jpg")
    dtimg = Image.open(base_img)
    
    need_height = drow_height-477
    needdt = math.ceil(need_height/477)
    drow_height = 1300+needdt*477
    
    im = Image.new("RGB", (600, drow_height), (255, 255, 255))
    
    for num in range(needdt):
        dtheight = 608 + int(num) * 477
        dtbox = (0, dtheight)
        im.paste(dtimg, dtbox)
    
    dtbox1 = (0, 0)
    im.paste(dtimg1, dtbox1)
    
    dtbox2 = (0, drow_height-692)
    im.paste(dtimg2, dtbox2)
    
    
    
    draw = ImageDraw.Draw(im)
    # 左上角开始
    x, y = 25, 608
    shulx = 1
    for msg in msg_list:
        if 'jpg' in str(msg) or 'png' in str(msg):
            iconarr = msg.split(',')
            picname = str(iconarr[0]) +".png"
            ICON_PATH = os.path.join(FILE_PATH,'icon')
            icon_name = os.path.join(ICON_PATH,picname)
            try:
                img = Image.open(icon_name).convert('RGBA')
            except FileNotFoundError:
                urllib.request.urlretrieve(iconarr[1], icon_name)
                img = Image.open(icon_name).convert('RGBA')

            if shulx%2 == 0:
                box = (110, y-60)
                #等比缩放要放入的图片
                img = img.resize((40, 40))
                #图片插入
                im.paste(img, box, mask=img.split()[3])
            else:
                box = (30, y+10)
                #等比缩放要放入的图片
                img = img.resize((60, 60))
                #图片插入
                im.paste(img, box, mask=img.split()[3])
                y += 80
                #print('原图片：长'+str(size[0])+'，宽'+str(size[1]))
                #print('后图片：长575，宽'+str(sf_height))
            shulx += 1
        else:
            drow_duanluo, drow_note_height, drow_line_height, drow_height = split_text(msg)
            for duanluo, line_count in drow_duanluo:
                draw.text((x, y), duanluo, fill=(0, 0, 0), font=font)
                y += drow_line_height * line_count
        
    bio  = io.BytesIO()
    im.save(bio, format='PNG')
    base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
    mes  = f"[CQ:image,file={base64_str}]"
    return mes


    
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
            mes = JsonAnalysis(GetInfo(uid, "cn_gf01"), uid, "cn_gf01")
            await bot.send(ev, mes, at_sender=True)
            #await bot.send_group_forward_msg(group_id=ev['group_id'], messages=tas_list)
        elif (uid[0] == "5"):
            sv.logger.info('原神查询uid中')
            mes = JsonAnalysis(GetInfo(uid, "cn_qd01"), uid, "cn_qd01")
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