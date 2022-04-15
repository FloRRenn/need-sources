from discord.ext import commands
import discord, urllib.parse
from discord.ext.commands.core import guild_only
from discord_components import *
from urllib.parse import urlparse, quote
from datetime import datetime

from bs4 import BeautifulSoup
from re import findall, search
from .Ultils.Language import *
from .Ultils.Guilds_Ultils import AllowToUseCommandInThisChannel, getLanguage, getAPI, checkLimitUsages
from .Ultils.Sauce import *
from .Ultils.TextWraper import shorten

import aiohttp, traceback

yandexHeader_1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cache-control': 'max-age=0',
    'cookie': 'yandexuid=1571059261641952985; is_gdpr=0; is_gdpr_b=CKm1JBD1Ww==; i=DjgJTTGxSmbU0wKZ66//ISHtySJWskpEtRkeeYqMI840HYRPFC/MchfaItZejgBNTLLfLJNUOGsnPg+psy4YD8VpvpA=; yp=1642557786.szm.1:1920x1080:1920x961; _yasc=GmKtODl8PXmpj5OWR016YrAOy2zCCoGllAPyO/YoAqA8R3SEgkA=; gdpr=0; _ym_uid=1641952987567972235; _ym_d=1641952988; cycada=DiVXCf4naSlM8tuaTVy1+DkAPen+S2PCroE54DtlGUY=',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
}

class Anime(commands.Cog):
    cookie = [
        'cbir-usage=panel%2Cview; yandexuid=4669755801634456845; is_gdpr=0; is_gdpr_b=CMS2BRCETCgC; mda=0; my=YwA=; _ym_uid=1638189205140798791; L=YjFmBGEEUW1mWFpzUl5aQ3h3Z3R8BmIHVxIqJxVWRlV2FQUgIA4DFlEkPA==.1639010592.14821.335198.c11a701c05fcb462e7471f81c08e42c7; yandex_login=avartar82@gmail.com; gdpr=0; i=b2n9T9UPBeNT9BuNV2+WWacD6oxmN4MfFLQgpiouxoVG27FgZ+L47Q8qoAhQi0hHw9uzTPvpOlibiUhNTrhMZxy8bXU=; yandex_gid=10553; Session_id=3:1640936042.5.0.1639010592500:t50EUayVskXBoLZjAAgCJA:5a.1.2:1|1528169755.-1.0.0:3.1:307520794|11:160243.733264.BND8vu88urMFgHTQcyhXGWMGiHQ; sessionid2=3:1640936042.5.0.1639010592500:t50EUayVskXBoLZjAAgCJA:5a.1.2:1|1528169755.-1.0.0:3.1:307520794|11:160243.733264.BND8vu88urMFgHTQcyhXGWMGiHQ; bltsr=1; Manganese=1; _yasc=fHst5Fn5FJ/qTTlutX45gqK/g8JJM+osSMN5rgH4n5nwJHjMs1VjVWecZ/V1Q1CX; yp=1954370592.udn.cDphdmFydGFyODJAZ21haWwuY29t#1643528039.ygu.1#1643465364.szm.1:1920x1080:1876x927',
        'cbir-usage=view; yandexuid=2918397771642860608; is_gdpr=0; is_gdpr_b=CKm1JBDxXQ==; i=ZfGkUZ5wci4f5nP/AnXU2MXWITAHXla+l6RYYDyK18EZX2b6bcBobNhRUAS72qAOZnhkKJkam51I9fsys9GjbE7AIz0=; yp=1643465408.szm.1:1920x1080:786x927; _yasc=Pq0jfXi853XjwtRDvQKHu51sIMgSo+mffd/+2mnKv1AdF++s9KI=; gdpr=0; _ym_uid=1642860610748229624; _ym_d=1642860610; bltsr=1; Manganese=1; _ym_isad=1',
        'cbir-usage=view; yandexuid=1571059261641952985; is_gdpr=0; is_gdpr_b=CKm1JBD1Ww==; i=DjgJTTGxSmbU0wKZ66//ISHtySJWskpEtRkeeYqMI840HYRPFC/MchfaItZejgBNTLLfLJNUOGsnPg+psy4YD8VpvpA=; _ym_uid=1641952987567972235; _ym_d=1641952988; yp=1643465619.szm.1:1920x1080:1920x916; _yasc=OIS7GGoGwMSp6h/p2sU23I/3ZMoabauxz9RShBijcOpeBU8Fc18=; gdpr=0; cycada=+iIIpQpsS9agSyMO6uBucwU5VrdtCWO2COjb5T4sojU=',
        'cbir-usage=panel%2Cview; yandexuid=2320670811643891575; is_gdpr=0; is_gdpr_b=CLWUVBCPYA==; i=nwsYnewWf/XIsRDrAtP0nG08TGx+NEwhoMYmxbCdiIg1z5l2j7VUJhhTLPCALh9dVyNiG5TgcZ+JN/vC7ywX3xIuzCY=; yp=1644496378.szm.1:1920x1080:1920x969; _yasc=HFDU3440NHQNrETbYD8VgPMvUHXXGnJKTmuNgcxdScvIBSO7iLE=; gdpr=0; _ym_uid=1643891582105958949; _ym_d=1643891582; cycada=u6TyUr0eP8o8RBZwQnSGWhUP4gmC/JLzSiUPgrOWV5Q=',
        'cbir-usage=view; yandexuid=1772175871643891829; is_gdpr=0; is_gdpr_b=CLWUVBCPYA==; i=o0Tor3S7KC1Fw0vHyvQEvMRKqznAQNsJMb+DvapYcZpEbqoJE9HN3cK33QCWCFRXboND35Q/YGiTIo3+ipTNCtcrbzg=; yp=1644496632.szm.1:1920x1080:1920x969; _yasc=A1xFk1RM0fPhI9x+GFdaE3NXjFXD9hzqml88xa0slGzxqHxqUt4=; gdpr=0; _ym_uid=1643891834477436026; _ym_d=1643891834'
    ]
    
    def __init__(self, bot):
        self.bot = bot
        self.headerGoogle = {
            "cookie": 'CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; 1P_JAR=2021-07-24-13; NID=219=07avD8_trNUJ29gu9xj0H1fBdCKY7Zl8b8wEyG5VIynOopoPsrQ_jP9Zsi8_0tNjLV4mbbAtUFqlzWPnkqirvgaRdgzio17_9knj7REf5FKjfuoYOftUv1qRq5Gu_9CLC-lQ-6wrZ55KkmVQsAx_xH7ihp09OGHgIoccjaMzDCE; DV=QyfJxeNryEEqcNh6fbLcG-i2nOiKrdc_b0uhmj4ilgIAAAA',
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            "x-client-data": 'CIq2yQEIprbJAQjBtskBCKmdygEInJbLAQjQmssBCKCgywEIrfLLAQjd8ssBCPDyywEI8PfLAQi0+MsBCJ75ywEI+fnLAQiw+ssBGI6eywEYuvLLAQ=='
        }
        
        self.headerYandex = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3,ja;q=0.2',
                'cache-control': 'max-age=0',
                'cookie': 'cbir-usage=panel%2Cview; yandexuid=4669755801634456845; is_gdpr=0; is_gdpr_b=CMS2BRCETCgC; mda=0; my=YwA=; _ym_uid=1638189205140798791; L=YjFmBGEEUW1mWFpzUl5aQ3h3Z3R8BmIHVxIqJxVWRlV2FQUgIA4DFlEkPA==.1639010592.14821.335198.c11a701c05fcb462e7471f81c08e42c7; yandex_login=avartar82@gmail.com; gdpr=0; i=b2n9T9UPBeNT9BuNV2+WWacD6oxmN4MfFLQgpiouxoVG27FgZ+L47Q8qoAhQi0hHw9uzTPvpOlibiUhNTrhMZxy8bXU=; yandex_gid=10553; Session_id=3:1640936042.5.0.1639010592500:t50EUayVskXBoLZjAAgCJA:5a.1.2:1|1528169755.-1.0.0:3.1:307520794|11:160243.733264.BND8vu88urMFgHTQcyhXGWMGiHQ; sessionid2=3:1640936042.5.0.1639010592500:t50EUayVskXBoLZjAAgCJA:5a.1.2:1|1528169755.-1.0.0:3.1:307520794|11:160243.733264.BND8vu88urMFgHTQcyhXGWMGiHQ; _ym_d=1641379985; bltsr=1; adequate=1; yp=1954370592.udn.cDphdmFydGFyODJAZ21haWwuY29t#1643528039.ygu.1#1642244898.szm.1:1920x1080:1876x927; _yasc=USTNs/UNvxkctm9zP3lwP9zeTF89l5Xa+boCD7UEbz2Q1PQc/MdwE2ohaCod86pE',
                'dnt': '1',
                'sec-ch-ua': '"CocCoc";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.84 Safari/537.36'
            }
        DiscordComponents(bot) 
        self.count = self.index = 0
        
    def _getCookie(self):
        if self.count == 3:
            self.count = 0
            
            if self.index == len(self.cookie) - 1:
                self.index = 0
            else:
                self.index += 1
        self.count += 1
        return self.cookie[self.index]
    
    def _ConvertTimestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d/%m/%Y')
    
    @commands.command()
    @commands.has_permissions(administrator = True, manage_channels = True, manage_guild = True)
    async def timestamp(self, ctx):
        await ctx.reply(datetime.now())
        
        
    @commands.command(aliases = ['s', 'S', 'a', 'A', 'Source', 'source', 'Sauce', 'sauce'])
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(per = 900, rate = 3, type = commands.BucketType.user)
    async def anime(self, ctx, url_ : str = None):
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        check = await checkLimitUsages(ctx.message.guild.id, 'anime', 'limitAnime')
        if check[0] == False:
            timestamp = self._ConvertTimestamp(check[1]['timestamp'])
            await ctx.reply(comeLimitation(LANGUAGE, timestamp))
            return
        
        check = await AllowToUseCommandInThisChannel(ctx, 'anime')
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.reply(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        api = getAPI(ctx.message.guild.id)
        async with ctx.message.channel.typing():
            getInfo = await FindSauce(self.bot, ctx, api, url_, ctx.message.attachments, LANGUAGE)
            
            try:
                if getInfo[0] == 50 or getInfo[0] == 60:
                    data = getInfo[1]
                    url = webName = None
                    creator = source = material = ''
                    
                    MoreButton = []
                    if 'similarity' in data['header']:
                        similarity = float(data['header']['similarity'])
                        mess = ''
                        if similarity < 60:
                            link = quote(getInfo[2], safe = '')
                            
                            GGIMAGE = f'https://www.google.com/searchbyimage?image_url={link}&safe=off'
                            YANDEX = f'https://yandex.com/images/search?url={link}&rpt=imageview'
                            ASCII2D = f'https://ascii2d.net/search/url/{link}'
                            TRACEMOE = f'https://trace.moe/?url={link}'
                            
                            yandex = Button(style = ButtonStyle.URL, label = 'Yandex', url = YANDEX, emoji = '1️⃣')
                            google = Button(style = ButtonStyle.URL, label = 'Google', url = GGIMAGE, emoji = '2️⃣')
                            ascii2d = Button(style = ButtonStyle.URL, label = 'Ascii2D', url = ASCII2D, emoji = '1️⃣')
                            tracemoe = Button(style = ButtonStyle.URL, label = 'Tracemoe', url = TRACEMOE, emoji = '2️⃣')
                            MoreButton = [[yandex, google], [ascii2d, tracemoe]]
                            yandexData = YandexCrawl(YANDEX, self._getCookie())
                            
                            if yandexData:
                                MessageLang = NotFoundSource(LANGUAGE)
                                saveSauce = Button(style = ButtonStyle.blue, label = MessageLang[4]) 
                                MoreButton[0].append(saveSauce)
                                mess = MessageLang[0]
                                
                                show = discord.Embed(title = f'{MessageLang[1]}', description = '- - - - - - - - - - - - ', color = 0xD35400)
                                
                                if yandexData:
                                    show.add_field(name = MessageLang[2], value = yandexData['url'], inline = True)
                                    show.set_image(url = yandexData['thumb'])
                                    
                                show.set_footer(text = MessageLang[3])
                                show.set_thumbnail(url = 'https://i.imgur.com/LaGVJ8A.png') 
                                
                                await ctx.reply(embed = show, components = MoreButton)
                                await ctx.reply(content = mess)
                                return
                        
                        listButtons = []   
                        MessageLang = FoundSource(LANGUAGE) 
                        saveSauce = Button(style = ButtonStyle.blue, label = MessageLang[8]) 
                        
                        show = discord.Embed(title = f'{MessageLang[0]} {similarity}%', description = '- - - - - - - - - - - - ', color = 0x6C3483)
                        
                        show.set_image(url = data['header']['thumbnail'])

                        if "creator" in data['data']:
                            creator = data["data"]["creator"]
                            show.add_field(name = MessageLang[1], value = f'`{str(creator).title()}`', inline = False)
                        
                        elif 'twitter_user_handle' in data['data']:
                            creator = data['data']['twitter_user_handle']
                            show.add_field(name = MessageLang[1], value = f'`{str(creator).title()}`', inline = False)
                            
                        elif 'member_name' in data['data']:
                            creator = data['data']['member_name']
                            show.add_field(name = MessageLang[1], value = f'`{str(creator).title()}`', inline = False)

                        if 'characters' in data["data"]:
                            characters = data['data']['characters']
                            if characters != '':
                                show.add_field(name = MessageLang[2], value = f'`{characters.title()}`', inline = True)
                            
                        if 'source' in data['data']:
                            source = data['data']['source']
                            
                            if 'i.pximg.net' in source:
                                pixivID = source.split('/')[-1]
                                url = 'https://www.pixiv.net/en/artworks/' + pixivID
                                webName = 'Pixiv'
                            
                            elif data['data']['source'] != '':
                                show.add_field(name = MessageLang[3], value = source, inline = False)    
                                
                        if  'index_name' in data['header']:
                            if 'E-Hentai' in data['header']['index_name']:
                                try:
                                    getHash = findall('[a-zA-Z0-9_.+-]+\.jpg', data['header']['index_name'])[0]
                                    getHash  = getHash.replace('.jpg', '&f_sh=on')
                                    url = 'https://e-hentai.org/?f_shash=' + getHash
                                    webName = 'E-Hentai'
                    
                                    query =quote(source, safe = '')
                                    gg = Button(style = ButtonStyle.URL, label = 'Google', url = 'https://www.google.com/search?q=' + query)
                                    listButtons.append(gg)
                                    
                                except:
                                    pass
                                            
                        if 'material' in data['data']:
                            material = data['data']['material']
                            if material != '':
                                show.add_field(name = MessageLang[4], value = f'`{material.title()}`', inline = False)
                            
                        if 'part' in data['data']:
                            part = str(data['data']['part'])
                            if part != '':
                                show.add_field(name = MessageLang[5], value = f'`{part}`', inline = True)
                                
                            watch = Button(style = ButtonStyle.URL, label = MessageLang[9], url = 'https://www.google.com/search?q=' + quote(source[:150] + ' part ' + part, safe = ''))
                            listButtons.append(watch)

                        if "est_time" in data['data']:
                            est_time = data['data']['est_time']
                            if est_time != '':
                                show.add_field(name = MessageLang[6], value = f'`{est_time}`', inline = True)
                        
                        if "ext_urls" in data['data'] and url == None:
                            url = data["data"]["ext_urls"][0]
                            webName = (urlparse(url).netloc).replace('www.', '')
                            
                        elif url == None:
                            query = str(creator) + ' ' + source + ' ' + material
                            if len(query) > 200:
                                creator = str(creator).replace("'", '')
                                query = shorten(creator, width = abs(200 - len(' ' + source + ' ' + material)), placeholder = "...") + ' ' + source + ' ' + material

                            query = quote(query, safe = '')
                            url = 'https://www.google.com/search?q=' + query
                            webName = 'Google'
                        
                        show.add_field(name = '- - - - - - - - - - - - - - -', value = f'[Link]({url})', inline = False)

                        button = Button(style = ButtonStyle.URL, label = webName, url = url)
                        listButtons.append(button)
                        listButtons.append(saveSauce)
                        await ctx.reply(embed = show, components = [listButtons])
                        
                        if similarity < 60:
                            await ctx.reply(MessageLang[7], components = MoreButton)

                    else:
                        show = discord.Embed(title = 'Rất tiếc, tui không tìm thấy nguồn của bức ảnh này', color = 0xFF0606)
                        await ctx.reply(embed = show)
                    
                elif getInfo[0] == 61:
                    link = quote(getInfo[2], safe = '')
                    YANDEX = f'https://yandex.com/images/search?url={link}&rpt=imageview'
                    yandexData = YandexCrawl(YANDEX, self._getCookie())
                    
                    MessageLang = NotFoundSource(LANGUAGE)
                    saveSauce = Button(style = ButtonStyle.blue, label = MessageLang[4]) 
                    
                    if yandexData:
                        show = discord.Embed(description = '- - - - - - - - - - - - ', color = 0x6C3483)
                        show.add_field(name = MessageLang[2], value = yandexData['url'], inline = True)
                        show.set_image(url = yandexData['thumb'])
                        await ctx.reply(embed = show, components = [saveSauce])
                        
                    else:
                        await ctx.reply('**Nothing Found**')
                    
                elif getInfo[0] == 51:
                    channel = self.bot.get_channel(930659053095497768)
                    with open('frame.jpg', 'rb') as f:
                        picture = discord.File(f)
                        msg = await channel.send(file = picture, delete_after = 30)
                        
                    link = quote(msg.attachments[0].url, safe = '')
                    YANDEX = f'https://yandex.com/images/search?url={link}&rpt=imageview'
                    yandexData = YandexCrawl(YANDEX, self._getCookie())
                    
                    MessageLang = NotFoundSource(LANGUAGE)
                    saveSauce = Button(style = ButtonStyle.blue, label = MessageLang[4]) 
                    
                    if yandexData:
                        show = discord.Embed(description = '- - - - - - - - - - - - ', color = 0x6C3483)
                        show.add_field(name = MessageLang[2], value = yandexData['url'], inline = True)
                        show.set_image(url = yandexData['thumb'])
                        await ctx.reply(embed = show, components = [saveSauce])
                    else:
                        await ctx.reply('**Nothing Found**')
                    
                else:
                    await ctx.reply(getInfo[1])
                    
            except Exception as e:
                myID = '<@660730514533122049>'
                await ctx.reply(UnknownErrorMess(LANGUAGE))
                
                channel = self.bot.get_channel(909404622278520872)
                content = f'{myID}, lỗi xuất hiện tại server **{ctx.message.guild.name} (ID: {ctx.message.guild.id})** trong kênh **{ctx.message.channel.name} (ID: {ctx.message.channel.id})** từ **{ctx.author}**'
                await channel.send(content)
                await channel.send(traceback.format_exc())
        
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(per = 1, rate = 3, type = commands.BucketType.user)
    async def src(self, ctx, link : str = None):
        check = await AllowToUseCommandInThisChannel(ctx, 'src')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.reply(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        try:
            image_link = getURL(link, ctx.message.attachments)
            MessageLang = ReverseSearch(LANGUAGE)
            
            if image_link:
                quote_link = urllib.parse.quote(image_link)
                async with ctx.message.channel.typing():
                    ggurl = 'https://images.google.com/searchbyimage?image_url=' + quote_link + '&safe=off'
                    SeeMore = Button(style = ButtonStyle.URL, label = MessageLang[0], url = ggurl)
                    ButtonListGG = [SeeMore]
                    
                    ydurl = 'https://yandex.com/images/search?url=' + quote_link + '&rpt=imageview'
                    MoreInfoButton = Button(style = ButtonStyle.URL, label = MessageLang[0], url = ydurl)
                    ButtonListYD = [MoreInfoButton]
                    
                    async with aiohttp.ClientSession(headers = self.headerGoogle) as session:
                        async with session.get(ggurl) as resp:
                            text = await resp.read()         
                              
                    show = discord.Embed(title = f'{MessageLang[2]} Google',  colour = 0x6C3483)
                    get_info = BeautifulSoup(text.decode('utf-8'), 'html5lib')
                    for i in get_info.find_all('div', class_ = 'g', limit = 5):
                        try:
                            data = i.find('div', class_ = 'yuRUbf')
                            url = data.find('a').attrs['href']
                            title = data.find('h3', class_ = 'LC20lb MBeuO DKV0Md').text
                            
                            show.add_field(name = title, value = url, inline = False)
                        except:
                            pass
                        
                    try:
                        image_raw = i.find('a', class_ = 'rGhul IHSDrd').attrs['href']
                        image_url = search("(?P<url>https?://[^\s]+)", image_raw).group("url").split('&imgrefurl=')
                        show.set_image(url = image_url[0])  
                    except:
                        pass
                        
                    try:
                        findMore = 'https://www.google.com' + get_info.find('div', id = 'Z6bGOb').find('a').attrs['href']
                        MoreButton = Button(style = ButtonStyle.URL, label = MessageLang[1], url = findMore)
                        ButtonListGG.append(MoreButton)
                    except:
                        pass
                    show.set_thumbnail(url = 'https://i.imgur.com/jZwQrKZ.gif')
                    show.set_footer(text = 'Powered by Google', icon_url = 'https://i.imgur.com/oaThOf4.png')
                    await ctx.reply(embed = show, components = [ButtonListGG]) 
                    
                    
                    async with aiohttp.ClientSession(headers = self.headerYandex) as session:
                        async with session.get(ydurl) as resp:
                            text = await resp.read()  
                    
                    get_info_1 = BeautifulSoup(text.decode('utf-8'), 'html5lib')  
                    show1 = discord.Embed(title = f'{MessageLang[2]} Yandex',  colour = 0xEC5C45)
                    count = 0
                    try:
                        for data in get_info_1.find_all('div', class_ = 'CbirSites-Item', limit = 5):
                            if count == 0:
                                thumdImage = data.find('div', class_ = 'CbirSites-ItemThumb').find('a').attrs['href']
                                count += 1
                                
                            info = data.find('div', class_ = 'CbirSites-ItemTitle')
                            title = info.text
                            urlDest = info.find('a').attrs['href']
                            show1.add_field(name = title, value = urlDest, inline = False)
                        show1.set_image(url = thumdImage)
                        show1.set_thumbnail(url = 'https://i.imgur.com/ZDhtIIJ.gif')
                    
                        MoreImagesYandex = 'https://yandex.com' + get_info_1.find('section', class_ = 'CbirItem CbirSimilar CbirSimilar_simple').find('a').attrs['href']
                        MoreImagesButton = Button(style = ButtonStyle.URL, label = MessageLang[1], url = MoreImagesYandex)
                    except:
                        show1.description = MessageLang[3]
                    show1.set_footer(text = 'Powered by Yandex', icon_url = 'https://i.imgur.com/MQBqhw5.png')
                    ButtonListYD.append(MoreImagesButton)
                    await ctx.reply(embed = show1, components = [ButtonListYD])
                        
            else:
                await ctx.reply(MessageLang[4])

        except Exception as e:
            pass
            
def setup(bot):
    bot.add_cog(Anime(bot))