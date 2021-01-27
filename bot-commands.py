import asyncio
import json
from random import randint

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import nekos

import config
from config import settings, text_channels, voice_channels, roles

bot = commands.Bot(settings['prefix'])


# The function prints info about user / member.
@bot.command()
async def info(ctx, member: discord.Member = None):
    with open('data.json', mode='r') as file:
        data = json.load(file)

    if member:
        emb = discord.Embed(title=f'Пользователь:   {member}', color=0xf68f79)

        emb.set_thumbnail(url=member.avatar_url)
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        emb.add_field(name='Создал аккаунт:  ', value=member.created_at.strftime("%d, %b, %Y"),
                      inline=True)
        emb.add_field(name='Присоединился к серверу:    ', value=member.joined_at.strftime("%d/%b/%Y"),
                      inline=True)
        emb.add_field(name='Money:', value=str(data[str(member.id)]['money']) + '∆', inline=True)
        emb.add_field(name='LVL:', value=str(data[str(member.id)]['lvl']) + '∆', inline=True)
        await ctx.message.channel.purge(limit=1)
        await ctx.send(embed=emb)

        property_of_user = ''
        for product in data[str(member.id)]['property']:
            property_of_user += ':**' + product + '**:    '

        emb = discord.Embed(title=f'Имущество: ', description=property_of_user, color=0xf68f79)
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title=f'Пользователь:   {ctx.author}', color=0xf68f79)

        emb.set_thumbnail(url=ctx.author.avatar_url)
        emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
        emb.add_field(name='Создал аккаунт:  ', value=ctx.author.created_at.strftime("%d, %b, %Y"),
                      inline=True)
        emb.add_field(name='Присоединился к серверу:    ', value=ctx.author.joined_at.strftime("%d/%b/%Y"),
                      inline=True)
        emb.add_field(name='Money:', value=str(data[str(ctx.author.id)]['money']) + '∆', inline=True)
        emb.add_field(name='LVL:', value=str(data[str(ctx.author.id)]['lvl']), inline=True)
        await ctx.message.channel.purge(limit=1)
        await ctx.send(embed=emb)

        property_of_user = ''
        for product in data[str(ctx.author.id)]['property']:
            property_of_user += ':**' + product + '**:    '

        emb = discord.Embed(title=f'Имущество: ', description=property_of_user, color=0xf68f79)
        await ctx.send(embed=emb)


# The function gives mute to the member.
@bot.command()
@commands.has_role('Модераторы')
async def mute(ctx, member: discord.Member, time=5, reason='Не понравился'):
    channel = bot.get_channel(id=text_channels['logi'])
    mute_role = discord.utils.get(ctx.guild.roles, id=roles["Mute"])

    emb = discord.Embed(title='Mute', color=0xff0000)

    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb.set_thumbnail(url=member.avatar_url)

    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
    emb.add_field(name='По причите:', value=reason)
    emb.add_field(name='На время:', value=str(time))

    await ctx.message.channel.purge(limit=1)
    await channel.send(embed=emb)
    await member.add_roles(mute_role)
    await asyncio.sleep(time * 60)

    emb = discord.Embed(title='Unmute', color=0xff0000)

    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb.set_thumbnail(url=member.avatar_url)

    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
    emb.add_field(name='По причите:', value=reason)
    await channel.send(embed=emb)
    await member.remove_roles(mute_role)


# The function gives unmutes to the member.
@bot.command()
@commands.has_role('Модераторы')
async def unmute(ctx, member: discord.Member, reason='Исправился'):
    channel = bot.get_channel(id=text_channels['logi'])
    mute_role = discord.utils.get(ctx.guild.roles, id=roles['Mute'])

    emb = discord.Embed(title='Unmute', color=0xff0000)

    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb.set_thumbnail(url=member.avatar_url)

    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
    emb.add_field(name='По причите:', value=reason)

    await ctx.message.channel.purge(limit=1)
    await channel.send(embed=emb)
    await member.remove_roles(mute_role)


# The function kicks the member.
@bot.command()
@commands.has_role('Модераторы')
async def kick(ctx, member: discord.Member, reason='Лох'):
    channel = bot.get_channel(id=text_channels['logi'])
    emb = discord.Embed(title='Kick', color=0xff0000)

    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb.set_thumbnail(url=member.avatar_url)

    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
    emb.add_field(name='По причите:', value=reason)

    await ctx.message.channel.purge(limit=1)
    await channel.send(embed=emb)
    await member.send(f'Вы были кикнуты с сервера по причине: {reason}')
    await member.kick()


# The function gives ban to a member.
@bot.command()
@commands.has_role('Модераторы')
async def ban(ctx, member: discord.Member, reason='Лох'):
    channel = bot.get_channel(id=text_channels['logi'])
    emb = discord.Embed(title='Ban', color=0xff0000)

    emb.set_author(name=ctx.message.author, icon_url=ctx.message.author.avatar_url)
    emb.set_thumbnail(url=member.avatar_url)

    emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
    emb.add_field(name='По причите:', value=reason)

    await ctx.message.channel.purge(limit=1)
    await channel.send(embed=emb)
    await member.send(f'Вы были забанены на сервере по причине: {reason}')
    await member.ban()


# The function just deletes the message.
@bot.command()
@commands.has_role('Модераторы')
async def c(ctx, amount=1):
    await ctx.message.channel.purge(limit=amount + 1)


def is_nsfw():
    async def predicate(ctx):
        return ctx.channel.is_nsfw()

    return commands.check(predicate)


nekos_arg = ['feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les',
             'wallpaper', 'lewdk', 'ngif', 'tickle', 'lewd', 'feed', 'gecg', 'eroyuri', 'eron', 'cum_jpg', 'bj',
             'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'gasm', 'poke', 'anal', 'slap', 'hentai', 'avatar',
             'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'lizard', 'pussy_jpg', 'pwankg',
             'classic', 'kuni', 'waifu', 'pat', '8ball', 'kiss', 'femdom', 'neko', 'spank', 'cuddle', 'erok',
             'fox_girl', 'boobs', 'random_hentai_gif', 'smallboobs', 'hug', 'ero', 'smug', 'goose', 'baka', 'woof']


# The function sends a hentai picture / gif.
@bot.command()
# @is_nsfw()
async def hen(ctx):
    emb = discord.Embed(title='Хентай', color=0xffffff)
    category = nekos_arg[randint(0, len(nekos_arg) - 1)]
    emb.set_image(url=nekos.img(category))

    await ctx.send(embed=emb)


# The function prints that bot is on.
@bot.event
async def on_ready():
    print('Bot was started')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Хентайщину'))


# The function creates a new voice channel once user is connected to the create room channel.
@bot.event
async def on_voice_state_update(member: discord.Member, before, after):
    if after.channel.id == voice_channels['Create_room']:
        for guild in bot.guilds:
            main_categories = discord.utils.get(guild.categories, id=voice_channels['channels'])
            channel2 = await guild.create_voice_channel(name=f'{member.display_name}', category=main_categories)
            await channel2.set_permissions(member, connect=True, mute_members=True, move_members=True,
                                           manage_channels=True)
            await member.move_to(channel2)

            def check(x, y, z):
                return len(channel2.members) == 0

            await bot.wait_for('voice_state_update', check=check)
            await channel2.delete()


# Variables for the economy
gift_time = 15
gift_money = 100
queue = []


# The function gives money to users if they ain't in (queue)
@bot.command()
async def timely(ctx):
    global gift_money

    with open('data.json', mode='r') as file:
        data = json.load(file)

    user_id = str(ctx.message.author.id)

    if user_id not in data:
        data[user_id] = {}
        data[user_id]['money'] = 100
        data[user_id]['property'] = []
        data[user_id]['lvl'] = 1
        data[user_id]['exp'] = 0
    else:
        lvl = int(data[user_id]['lvl'])
        gift_money *= lvl

    if user_id not in queue:
        data[user_id]['money'] += gift_money
        emb = discord.Embed(description=f'Вы получили на счет: {gift_money} монет!', color=0xffd500)
        await ctx.send(embed=emb)
        queue.append(user_id)

        with open('data.json', mode='w') as file:
            json.dump(data, file)

        await asyncio.sleep(gift_time * 60)
        queue.remove(user_id)
    else:
        emb = discord.Embed(description=f'Деньги можно получать каждые {gift_time} минут', color=0xffd500)
        await ctx.send(embed=emb)


# The function prints information about the balance of the user / member.
@bot.command()
async def balance(ctx, member: discord.Member = None):
    with open('data.json', mode='r') as file:
        data = json.load(file)

    user_id = str(ctx.message.author.id)

    if ctx.author == member or member is None:
        emb = discord.Embed(title=f'Ваш баланс: **{data[user_id]["money"]}**∆', color=0xffd500)
        await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title=f'Баланс участника {member.display_name}:'
                                  f' **{data[str(member.id)]["money"]}**∆', color=0xffd500)
        await ctx.send(embed=emb)


# The function gives money to a member.
# Admins and Moderators can give infinite money for members.
@bot.command()
async def gm(ctx, member: discord.Member, quantity=0):
    with open('data.json', mode='r') as file:
        data = json.load(file)

    user_id = str(ctx.author.id)
    member_id = str(member.id)

    admin_role = discord.utils.get(ctx.guild.roles, id=roles['Администратор'])
    moderator_role = discord.utils.get(ctx.guild.roles, id=roles['Модераторы'])
    if admin_role in ctx.author.roles or moderator_role in ctx.author.roles:
        data[member_id]['money'] += int(quantity)
        emb = discord.Embed(description=f'Вы перевели пользователю {member.display_name} **{quantity}** хуяксов',
                            color=0xffd500)
    else:
        if data[user_id]['money'] >= int(quantity):
            data[member_id]['money'] += int(quantity)
            data[user_id]['money'] -= int(quantity)

            emb = discord.Embed(description=f'Вы перевели пользователю {member.display_name} **{quantity}** хуяксов',
                                color=0xffd500)
        else:
            emb = discord.Embed(description=f'Иди нахуй, нищеброд!', color=0xffd500)

    await ctx.send(embed=emb)

    with open('data.json', mode='w') as file:
        json.dump(data, file)


# The functions prints list of items from the shop ('./shop.json').
@bot.command()
async def shop(ctx):
    with open('shop.json', mode='r') as file:
        shop_items = json.load(file)

    emb = discord.Embed(title='Shop', color=0xffd500)
    for product in shop_items:
        emb.add_field(name=f'{product}', value=shop_items[product]["price"], inline=False)

    await ctx.send(embed=emb)


# The function adds your product to the shop. Only Admins/Moderators can use it.
@commands.has_role('Модераторы')
@bot.command()
async def ap(ctx, product_name, price):
    with open('shop.json', mode='r') as file:
        shop_items = json.load(file)

    product_name = str(product_name)  # We need this action, because without it user can give value
    # of the product with a dot

    if product_name not in shop_items:
        shop_items[product_name] = {}
        shop_items[product_name]['price'] = int(price)

        emb = discord.Embed(description=f'Продукт: {product_name} был добавлен в магазин', color=0xffd500)
    else:
        emb = discord.Embed(description=f'Такой продукт уже есть в магазине!')

    await ctx.send(embed=emb)

    with open('shop.json', mode='w') as file:
        json.dump(shop_items, file)


# The function removes certain from the shop. Only Admins/Moderators can use it.
@bot.command()
@commands.has_role('Модераторы')
async def rp(ctx, product_name):
    with open('shop.json', mode='r') as file:
        shop_items = json.load(file)

    product_name = str(product_name)  # We need to make it because user can give a value with point

    if product_name in shop_items:
        del shop_items[product_name]
        emb = discord.Embed(description=f'Продукт: {product_name} был удален!')
    else:
        emb = discord.Embed(description=f'Такого продукта нет!')

    await ctx.send(embed=emb)

    with open('shop.json', mode='w') as file:
        json.dump(shop_items, file)


# The function lets user buy items in the shop.
@bot.command()
async def buy(ctx, product):
    with open('shop.json', mode='r') as file:
        shop_items = json.load(file)

    with open('data.json', mode='r') as file:
        data = json.load(file)

    user_id = str(ctx.author.id)
    product = str(product)

    if product in shop_items:

        if data[user_id]['money'] >= shop_items[product]['price']:

            if product not in data[user_id]['property']:
                emb = discord.Embed(title=f'Вы преобрели: {product}', color=0xff0000)
                data[user_id]['money'] -= shop_items[product]['price']
                data[user_id]['property'].append(product)
            else:
                emb = discord.Embed(title=f'У вас это уже есть!')
        else:
            emb = discord.Embed(title=f'Иди работай!', color=0xff0000)
    else:
        emb = discord.Embed(title=f'Такого у нас нет(', color=0xff0000)

    await ctx.send(embed=emb)

    with open('data.json', mode='w') as file:
        json.dump(data, file)


# The function lets user sell their property.
@bot.command()
async def sell(ctx, product_name):
    with open('shop.json', mode='r') as file:
        shop_items = json.load(file)

    with open('data.json', mode='r') as file:
        data = json.load(file)

    user_id = str(ctx.author.id)
    product_name = str(product_name)

    if product_name in data[user_id]['property']:
        if product_name in shop_items:
            index = data[user_id]['property'].index(product_name)
            return_price = shop_items[product_name]['price'] // 3

            data[user_id]['property'].pop(index)
            data[user_id]['money'] += return_price
            emb = discord.Embed(description=f'Вы продали: {product_name} за {return_price} хуяксов!',
                                color=0xffb700)
        else:
            emb = discord.Embed(description=f'Вы не можете продавать эксклюзивные предметы', color=0xff0000)
    else:
        emb = discord.Embed(description=f'У тебя нет такого, АЛО!', color=0xff0000)

    await ctx.send(embed=emb)

    with open('data.json', mode='w') as file:
        json.dump(data, file)


# The function starts 'game of numbers'.
@bot.command()
async def num(ctx, sign='==', val=50, bid=100):
    with open('data.json') as file:
        data = json.load(file)

    user_id = str(ctx.author.id)

    sign = '==' if sign == '=' else sign

    if val > 100 or val < 0:
        emb = discord.Embed(title='Пошел в Жопу, "Гени"')
    else:
        if data[user_id]['money'] >= bid:
            catch = randint(1, 100)
            expression = f'{catch}{sign}{val}'

            data[user_id]['money'] -= bid
            emb = discord.Embed(title='Игра началась', description=f'Вы поставили {bid}∆ на {sign} {val}',
                                color=0x5d00ff)
            await ctx.send(embed=emb)

            if eval(expression):
                if sign == '==':
                    emb = discord.Embed(title='JackPot!!!', description=f'Вы выйграли: {bid * 100 - bid}∆!'
                                                                        f'\nВыпало число: {catch}', color=0xff00fb)
                    data[user_id]['money'] += int(bid) * 100
                else:
                    if val > 50:
                        prize = int(val) if sign == '>' else 100 - int(val)
                    else:
                        prize = int(val) if sign == '>' else 100 - int(val)
                    prize = prize / 50 + 1
                    emb = discord.Embed(title='Победа!!!', description=f'Вы выйграли: {int(bid) * prize - int(bid)}∆!'
                                                                       f'\nВыпало число: {catch}', color=0x5d00ff)
                    data[user_id]['money'] += int(int(bid) * prize)
            else:
                emb = discord.Embed(title='Лооох!', description=f'Ты въебал: {bid}∆!'
                                                                f'\nВыпало число: {catch}', color=0xff0000)
        else:
            emb = discord.Embed(title='У тебя нет столько хуяксов!', color=0xff0000)

    await ctx.send(embed=emb)

    with open('data.json', 'w') as file:
        json.dump(data, file)


# The function prints the bot-commands.
@bot.command()
async def h(ctx):
    emb = discord.Embed(name='Правила сервера:', color=0x00fff7)

    emb.add_field(name='!h', value='Узнать комманды бота', inline=False)
    emb.add_field(name='!info (@Имя пользователя)', value='Узнать информацию о переданном пользователе', inline=False)
    emb.add_field(name='!hen', value='Рандомная хентайка<)', inline=False)
    emb.add_field(name='!timely', value='Получить деньги(раз в 15 минут)', inline=False)
    emb.add_field(name='!balance (@Имя пользователя)', value='Узнать текущий баланс', inline=False)
    emb.add_field(name='!gm [@Имя пользователя] [Сколько хотите перевести]', value='Передать деньги пользователю',
                  inline=False)
    emb.add_field(name='!shop', value='Посмотреть магазин', inline=False)
    emb.add_field(name='!buy [Название товара]', value='Купить предмет', inline=False)
    emb.add_field(name='!sell [Название товара]', value='Продать предмет', inline=False)
    emb.add_field(name='!num [>/</=] [Какого числа] [Сумма ставки]', value='Игра: "Больше/Меньше"', inline=False)
    emb.set_footer(text='Аргументы передаются без скобок!')

    await ctx.send(embed=emb)


# The function prints the Admin/Moderator bot-commands.
@bot.command()
@commands.has_role('Модераторы')
async def ha(ctx):
    emb = discord.Embed(name='Правила сервера:', color=0x00ff22)

    emb.add_field(name='!mute [@Имя пользователя] (время) (причина)',
                  value='Выдать мут нарушителю', inline=False)
    emb.add_field(name='!unmute [@Имя пользователя] (причина)',
                  value='Размутить пользователя', inline=False)
    emb.add_field(name='!kick [@Имя пользователя] (причина)',
                  value='Кикнуть нарушителя с сервера', inline=False)
    emb.add_field(name='!ban [@Имя пользователя] (причина)',
                  value='Забанить нарушителя', inline=False)
    emb.add_field(name='!с (Количество)',
                  value='Удалить переданное количество сообщений', inline=False)
    emb.add_field(name='!ap [Название продукта] [стоимость]',
                  value='Добавить продукт в магазин', inline=False)
    emb.add_field(name='!rp [Название продукта]',
                  value='Удалить продукт из магазина', inline=False)
    emb.set_footer(text='Параметры написанные в скобках можно не передовать.')

    await ctx.send(embed=emb)


bot.run(settings['token'])
