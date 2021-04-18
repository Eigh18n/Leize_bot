from hoshino import Service


sv = Service("原神帮助")


help_txt = '''「卢皮卡」想要了解我，我会的，不多。
https://shimo.im/docs/9RwRHRyqk8ptgCRt
'''


@sv.on_fullmatch("雷泽帮助")
async def help1(bot, ev):
    await bot.send(ev, help_txt)

@sv.on_fullmatch("雷泽功能")
async def help2(bot, ev):
    await bot.send(ev, help_txt)

@sv.on_fullmatch("雷泽菜单")
async def help3(bot, ev):
    await bot.send(ev, help_txt)

@sv.on_fullmatch("雷泽会什么")
async def help4(bot, ev):
    await bot.send(ev, help_txt)