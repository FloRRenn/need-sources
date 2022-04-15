from discord.ext import commands, tasks
import discord, requests, random, json, time, asyncpg
from discord.ext.commands.core import command, guild_only
from discord_components import *
from googletrans import Translator
from random import choice

from .Ultils.Boooru import BooruImage as booru
from .Ultils.Language import *
from .Ultils.Guilds_Ultils import AllowToUseCommandInThisChannel, getLanguage, isLoli
from .Ultils import Hentai_Ultils as hentai_ultils 
        
from hentai import Hentai, Format, Utils, Sort

username = 'florren'#os.environ.get("USERNAME")
password = 'florren2k2'#os.environ.get("PASSWORD")

loli_link = [
    'https://cdn.discordapp.com/attachments/939741673930510368/939741767639646218/5_Great_anime_memes_-_Otaku_Diary.jpg',
    'https://i.imgur.com/rvcVlal.png',
    'https://cdn.discordapp.com/attachments/939741673930510368/939741776468672562/FBI_MOMENT_-_Savieo_-_Save.mp4',
    'https://cdn.discordapp.com/attachments/939741673930510368/939741785243123732/Gifts_with_Sound_-_Savieo_-_Save.mp4',
    'https://cdn.discordapp.com/attachments/939741673930510368/939741786425950255/FBI_Open_Up_LOLI_meme_2.webm',
    'https://cdn.discordapp.com/attachments/939741673930510368/939741820563382302/loli_dance_totally_not_an_FBI_bait_-_Savieo_-_Save.mp4',
    'https://cdn.discordapp.com/attachments/939741673930510368/939741827974709248/Loli_FBI_-_Savieo_-_Save.mp4',
    'https://cdn.discordapp.com/attachments/939741673930510368/939741881959612426/what_the_fuck_is_this_-_-_Savieo_-_Save.mp4'
]

class Entertainment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.PrevSearchRule34 = self.PrevResultsRule34 = None
        
        self.DelCommic.add_exception_type(asyncpg.PostgresConnectionError)
        self.DelCommic.start()
        
    @tasks.loop(hours = 1)
    async def DelCommic(self):
        await hentai_ultils.delCommic()
        
    @DelCommic.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
        
    @commands.command(aliases = ['Loli', 'Lolicon', 'Lolita', 'lolicon', 'lolita'])
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(3, 120, commands.BucketType.user)
    async def loli(self, ctx):
        await ctx.send(choice(loli_link))
        
        channel = self.bot.get_channel(909404622278520872)
        await channel.send(f'**{ctx.author}** đã tìm kiếm Loli trong server **{ctx.message.guild.name}** tại kênh **{ctx.message.channel.name}**')
        
    @commands.command(aliases = ['rule', 'r34'])
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def rule34(self, ctx, *, value : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'rule34')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        if value == '':
            await ctx.send(BooruError('rule34', LANGUAGE))
            return
        
        
        value = value.lower().strip()
        value = value.replace(' ', '_')

        if isLoli(value) == True:
            await self.loli(ctx)
            return
        
        if self.PrevSearchRule34 != value or len(self.PrevResultsRule34) == 0:
            baseURL = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags=' + value + '%20~'
            resp = requests.get(baseURL)
            try:
                data = json.loads(resp.content)
            except:
                await ctx.send(rule34Mess(LANGUAGE))
                return
            
            self.PrevSearchRule34 = value
            self.PrevResultsRule34 = data
            
        check = False
        for i in range (min(3, len(self.PrevSearchRule34))):
            try:
                index = random.randint(0, len(self.PrevResultsRule34) - 1)
                randomContent = self.PrevResultsRule34[index]
                self.PrevResultsRule34.pop(index)
                
                if not randomContent['file_url'].endswith('.mp4'):
                    splitTag = randomContent["tags"].split(' ')
                    realTags = ' '.join([f'`{i}`' for i in splitTag if value in i])
                    
                    show = discord.Embed(color = 0x6C3483)
                    show.add_field(name = 'Tags' , value = realTags, inline = False)
                    show.set_image(url = randomContent['sample_url'])
                    show.set_footer(text = 'Author: ' + str(randomContent['owner']))
                    
                    Save_Button = Button(style = ButtonStyle.blue, label = SaveImage(LANGUAGE))
                    
                    await ctx.send(embed = show, components = [[Save_Button]])
                    
                else:
                    Video_Save_Button = Button(style = ButtonStyle.blue, label = SaveVideo(LANGUAGE))
                    await ctx.send(randomContent['file_url'], components = [[Video_Save_Button]])
                check = True
                    
            except:
                pass
        
        if check == False:
            await ctx.send(BooruError('rule34', LANGUAGE))
        
    @commands.command(aliases = ['q', 'quote'])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    async def quotes(self, ctx, animeName = None):
        check = await AllowToUseCommandInThisChannel(ctx, 'quote')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        baseURL = 'https://animechan.vercel.app/api/'
        translator = Translator()
        
        def quote():
            url = baseURL + 'random'
            resp = requests.get(url)
            data = json.loads(resp.content)
            return data
        
        async with ctx.message.channel.typing():
            if animeName == None:
                data = quote()
                while len(data['quote']) > 1024:
                    data = quote()
                    
                trans = translator.translate(data['quote'], dest='vi')
                show = discord.Embed(description = data['quote'], color = 0x6C3483)
                show.set_author(name = f"`{data['character']}` trong bộ `{data['anime']}`")
                show.add_field(name = 'Tạm dịch', value = f'```{trans.text}```', inline = False)
                await ctx.send(embed = show)          
    
    @commands.command(aliases = ['id', 'henbyid', 'henid', 'hentaiid'])        
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def readHentaibyID(self, ctx, id : int = None, isTag : bool = False):
        check = await AllowToUseCommandInThisChannel(ctx, 'henbyid')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        async with ctx.message.channel.typing():
            check = id
            mess = HentaiMess(id, LANGUAGE)
            
            if id == None:
                while True:
                    checkLoli = False
                    tag = ''
                    id = Utils.get_random_id()
                    
                    doujin = Hentai(id)
                    for i in doujin.tag:
                        if isLoli(i.name) == True:
                            checkLoli = True
                            
                        tag += f'` {i.name} ` '
                        
                    if checkLoli == False:
                        break             
                
            elif not Hentai.exists(id):
                await ctx.send(mess[0])
                return
        
            if check != None :
                doujin = Hentai(id)
                tag = ''
                for i in doujin.tag:
                    if isLoli(str(i.name)) and isTag == False:
                        await ctx.send(mess[1])
                        return
                    
                    tag += f'`{i.name}` '          
            
            title = doujin.title(Format.Pretty)
            imageList = doujin.image_urls
            info = doujin.artist

            if len(info) != 0:
                hyperlink = f'[{info[0].name.title()}]({info[0].url})'

            elif len(info) == 0:
                hyperlink = 'N/A'
                
            length = len(imageList)
            
            show = discord.Embed()
            show.add_field(name = mess[2], value = f'[{title}](https://nhentai.net/g/{id})', inline = True)
            show.add_field(name = mess[3], value = hyperlink, inline = False)
            show.add_field(name = mess[4], value = length, inline = True)
            show.add_field(name = 'ID', value = id, inline = True)
            show.add_field(name = 'Tag', value = tag, inline = False)
            show.set_image(url = doujin.cover)
            
            if isTag == False:
                show.set_footer(text = mess[5])    
                msg = await ctx.send(embed = show)
                
                emoji = ['💾', '🔽']
                for emo in emoji:
                    await msg.add_reaction(emo) 
                
            elif isTag == True:
                show.set_footer(text = mess[6])    
                msg = await ctx.send(embed = show)
                
                emoji = ['⬅️', '➡️']
                for emo in emoji:
                    await msg.add_reaction(emo)
                return ctx.message.guild.id     
        
            infoCommic = {
                'ID' : ctx.message.guild.id,
                'IDcommic' : id,
                'link' : f'https://nhentai.net/g/{id}',
                'title' : title,
                'lenght' : length,
                'currentPage' : 0,
                'imageList' : imageList,
                'timestamp' : time.time(),
                'lang' : LANGUAGE
            }
            await hentai_ultils.addCommic(infoCommic, ctx.message.guild.id)            

    @commands.command(aliases = ['henbytag', 'hentag', 'hentaitag'])        
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 5, commands.BucketType.user)  
    async def readHentaibyTAG(self, ctx, *, tag : str):
        check = await AllowToUseCommandInThisChannel(ctx, 'henbytag')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.strip()
        tag = tag.lower()
        async with ctx.message.channel.typing():
            if isLoli(tag) == True:
                await self.loli(ctx)
                return
            
            get = Utils.search_by_query(tag, sort=Sort.PopularWeek)
            listID = []
            
            for i in get:
                listID.append(i.id)
            
            if listID:
                msg = await self.readHentaibyID(ctx, listID[0], True)
                await hentai_ultils.addListIDHen(ctx.message.guild.id, listID, LANGUAGE)
                
            else:
                await ctx.send(HentaiTagError(tag, LANGUAGE))
                
    @commands.command(aliases = ['nbooru'])        
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def NSFWbomb(self, ctx, *, tag : str = ''): 
        check = await AllowToUseCommandInThisChannel(ctx, 'nbomb')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        async with ctx.message.channel.typing():
            tag = tag.lower().strip() 
            if tag != '' and isLoli(tag) == True:
                await self.loli(ctx)
                return
            
            data = await booru.Booru(tag, False)      
            
            check = False
            Save_Button = Button(style = ButtonStyle.blue, label = SaveImage(LANGUAGE)) 
            Video_Save_Button = Button(style = ButtonStyle.blue, label = SaveVideo(LANGUAGE))
            for i in data:
                if i:
                    if not i.endswith('.mp4') and not i.endswith('.webm') and not i.endswith('.mov'):
                        show = discord.Embed(color = 0x6C3483)  
                        show.set_image(url = i)        
                        await ctx.send(embed = show, components = [Save_Button])
                        
                    else:
                        await ctx.send(i, components = [Video_Save_Button])
                    check = True
                
            if check == False:
                await ctx.send(BooruError('nbooru', LANGUAGE))
    
    async def BooruSend(self, cmd : str, ctx, image, LANGUAGE):
        if image != None:
            if not image.endswith('.mp4') and not image.endswith('.webm'):
                Save_Button = Button(style = ButtonStyle.blue, label = SaveImage(LANGUAGE)) 
                show = discord.Embed(color = 0x6C3483)
                show.set_image(url = image)
                await ctx.send(embed = show, components = [Save_Button])
                
            else:
                Video_Save_Button = Button(style = ButtonStyle.blue, label = SaveVideo(LANGUAGE))
                await ctx.send(image = image, components = [Video_Save_Button])
                
        else:
            await ctx.send(BooruError(cmd, LANGUAGE))
    
    @commands.command(aliases = ['ngel'])        
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def ngelbooru(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'ngelbooru')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Gel(tag, False)
            await self.BooruSend('ngelbooru', ctx, image, LANGUAGE) 
        
    @commands.command(aliases = ['ndan'])        
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def ndanbooru(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'ndanbooru')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Dan(tag, False)
            await self.BooruSend('ndanbooru', ctx, image, LANGUAGE) 
        
    @commands.command(aliases = ['nyan'])        
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def nyandere(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'nyandere')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Yande(tag, False)
            await self.BooruSend('nyandere', ctx, image, LANGUAGE)   
        
    @commands.command(aliases = ['nkona'])        
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def nkonachan(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'nkonachan')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Kona(tag, False)
            await self.BooruSend('nkoanchan', ctx, image, LANGUAGE)   
    
    @commands.command(aliases = ['booru'])        
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def SFWbomb(self, ctx, *, tag : str = ''): 
        check = await AllowToUseCommandInThisChannel(ctx, 'bomb')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        async with ctx.message.channel.typing():
            tag = tag.lower().strip() 
            if tag != '' and isLoli(tag) == True:
                await self.loli(ctx)
                return
            
            data = await booru.Booru(tag, True)      
            
            check = False
            Save_Button = Button(style = ButtonStyle.blue, label = SaveImage(LANGUAGE)) 
            Video_Save_Button = Button(style = ButtonStyle.blue, label = SaveVideo(LANGUAGE))
            for i in data:
                if i:
                    if not i.endswith('.mp4') and not i.endswith('.webm'):
                        show = discord.Embed(color = 0x6C3483)  
                        show.set_image(url = i)        
                        await ctx.send(embed = show, components = [Save_Button])
                        
                    else:
                        await ctx.send(i, components = [Video_Save_Button])
                    check = True
                
            if check == False:
                await ctx.send(BooruError('booru', LANGUAGE))
    
    @commands.command(aliases = ['gel'])        
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def gelbooru(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'ngelbooru')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Gel(tag, True)
            await self.BooruSend('gelbooru', ctx, image, LANGUAGE) 
        
    @commands.command(aliases = ['dan'])        
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)   
    async def danbooru(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'danbooru')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Dan(tag, True)
            await self.BooruSend('danbooru', ctx, image, LANGUAGE) 
        
    @commands.command(aliases = ['yan'])        
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)  
    async def yandere(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'yandere')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Yande(tag, True)
            await self.BooruSend('yandere', ctx, image, LANGUAGE)   
        
    @commands.command(aliases = ['kona'])        
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)   
    async def konachan(self, ctx, tag : str = ''):
        check = await AllowToUseCommandInThisChannel(ctx, 'konachan')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        tag = tag.lower().strip()
        if tag != '' and isLoli(tag) == True:
            await self.loli(ctx)
            return
        
        async with ctx.message.channel.typing():
            image = await booru.Kona(tag, True)
            await self.BooruSend('koanchan', ctx, image, LANGUAGE)   
        
def setup(bot):
    bot.add_cog(Entertainment(bot))