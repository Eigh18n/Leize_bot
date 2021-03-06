import random

from nonebot import on_command

from hoshino import R, Service, priv, util




# basic function for debug, not included in Service('chat')
@on_command('zai?', aliases=('在?', '在？', '在吗', '在么？', '在嘛', '在嘛？'), only_to_me=True)
async def say_hello(session):
    await session.send('我在，朋友。')

sv = Service('chat', visible=False)

@sv.on_fullmatch('雷泽')
async def say_calling(bot, ev):
    await bot.send(ev, random.choice(['你的气味···好闻。一起狩猎吧！','唔，兔子的味道…','风...唔...舒服。','我是狼。人的爸爸、妈妈，没有。','你是朋友，我和你一起狩猎。']), at_sender=True)

@sv.on_fullmatch(('早', '早上好', '早安', '早啊'))
async def say_morning(bot, ev):
    await bot.send(ev, '太阳出来了。狩猎一起去？', at_sender=True)

@sv.on_fullmatch(('午安', '中午好', '午好'))
async def say_afternoon(bot, ev):
    await bot.send(ev, '大块吃肉，开心！', at_sender=True)

@sv.on_fullmatch(('晚', '晚好', '晚安', '晚上好', '群晚安', '睡了'))
async def say_night(bot, ev):
    await bot.send(ev, random.choice(['你去睡觉吧，我看月亮。', '你睡觉，我看守，明天一起狩猎。']), at_sender=True)

@sv.on_fullmatch(('丽莎'))
async def say_member1(bot, ev):
    await bot.send(ev, '师父的雷，天空会变黑。很可怕，很强。')

@sv.on_fullmatch(('迪卢克'))
async def say_member2(bot, ev):
    await bot.send(ev, '迪卢克，红红的、黑黑的。又冷又热。')

@sv.on_fullmatch(('芭芭拉'))
async def say_member3(bot, ev):
    await bot.send(ev, '芭芭拉，亮晶晶的女孩子。很善良。')

@sv.on_fullmatch(('温迪'))
async def say_member4(bot, ev):
    await bot.send(ev, '诗歌…嗯...不明白。虽然不明白，「卢皮卡」喜欢。')

@sv.on_fullmatch(('班尼特'))
async def say_member5(bot, ev):
    await bot.send(ev, '班尼特，话很多，和他一起，吃不饱。')

@sv.on_fullmatch(('可莉'))
async def say_member6(bot, ev):
    await bot.send(ev, '可莉，朋友。朋友，但是，头疼。')

@sv.on_prefix("群发")
async def message_all(bot, ev):
    if priv.check_priv(ev, priv.SUPERUSER):
        txt = ev.message.extract_plain_text().strip().lower()
        if txt == "":
            return
        await sv.broadcast(txt, 'all', 0)
    else:
        return

# @sv.on_fullmatch(('老婆', 'waifu', 'laopo'), only_to_me=True)
# async def chat_waifu(bot, ev):
#     if not priv.check_priv(ev, priv.SUPERUSER):
#         await bot.send(ev, R.img('laopo.jpg').cqcode)
#     else:
#         await bot.send(ev, 'mua~')


# @sv.on_fullmatch('老公', only_to_me=True)
# async def chat_laogong(bot, ev):
#     await bot.send(ev, '你给我滚！', at_sender=True)


@sv.on_fullmatch('mua', only_to_me=True)
async def chat_mua(bot, ev):
    await bot.send(ev, '还...从来，没有人，对我这么好...', at_sender=True)


@sv.on_fullmatch('来点星奏')
async def seina(bot, ev):
    await bot.send(ev, R.img('星奏.png').cqcode)


# @sv.on_fullmatch(('我有个朋友说他好了', '我朋友说他好了', ))
# async def ddhaole(bot, ev):
#     await bot.send(ev, '那个朋友是不是你弟弟？')
#     await util.silence(ev, 30)


# @sv.on_fullmatch('我好了')
# async def nihaole(bot, ev):
#     await bot.send(ev, '不许好，憋回去！')
#     await util.silence(ev, 30)


# ============================================ #


# @sv.on_keyword(('确实', '有一说一', 'u1s1', 'yysy'))
# async def chat_queshi(bot, ctx):
#     if random.random() < 0.05:
#         await bot.send(ctx, R.img('确实.jpg').cqcode)


# @sv.on_keyword(('会战'))
# async def chat_clanba(bot, ctx):
#     if random.random() < 0.02:
#         await bot.send(ctx, R.img('我的天啊你看看都几度了.jpg').cqcode)


# @sv.on_keyword(('内鬼'))
# async def chat_neigui(bot, ctx):
#     if random.random() < 0.10:
#         await bot.send(ctx, R.img('内鬼.png').cqcode)

# nyb_player = f'''{R.img('newyearburst.gif').cqcode}
# 正在播放：New Year Burst
# ──●━━━━ 1:05/1:30
# ⇆ ㅤ◁ ㅤㅤ❚❚ ㅤㅤ▷ ㅤ↻
# '''.strip()

# @sv.on_keyword(('春黑', '新黑'))
# async def new_year_burst(bot, ev):
#     if random.random() < 0.02:
#         await bot.send(ev, nyb_player)
