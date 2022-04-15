from bs4 import BeautifulSoup

from urllib.parse import quote
from .Ultils.Language import AllowToUseCommand, DebutMess, JAVmess, FACEmess, RandomMovieMess
from .Ultils.Guilds_Ultils import AllowToUseCommandInThisChannel, getLanguage, checkLimitUsages
from .Ultils.JAV_Sauce import *

from discord.ext import commands
import discord, os, time, asyncio, re
from datetime import datetime
from discord.ext.commands.core import guild_only
from discord_components import *

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

letterNum = "`3P`, `4P`, `69`"
letterA = "`AV Actress`, `Abuse`, `Affair`, `Amateur`, `Anal`, `Anchorwoman`"
letterB = "`BBW`, `Bath`, `Beautiful Girl`, `Beauty Shop`, `Best`, `Big Tits`, `Black Actor`, `Blazer`, `Bloomers`, `Blowjob`, `Blu-ray`, `Body Conscious`, `Bondage`, `Booth Girl`, `Breast Milk`, `Breasts`, `Bride`, `Bukkake`, `Bunny Girl`, `Busty Fetish`, `Butt`"
letterC = "`Car Sex`, `Catgirl`, `Cervix`, `Close Up`, `Conceived`, `Confinement`, `Cosplay`, `Couple`, `Cowgirl`, `Creampie`, `Cross Dressing`, `Cuckold`, `Cum`, `Cunnilingus`"
letterD = "`Dance`, `Dead Drunk`, `Debut Production`, `Deep Throating`, `Delusion`, `Digital Mosaic`, `Dirty Words`, `Documentary`, `Drama`, `Drug`"
letterE = "`Egg Vibrator`, `Electric Massage`, `Enema`, `Entertainer`, `Erotic Wear`, `Evil`, `Exposure`"
letterF = "`Face Sitting`, `Facials`, `Fan Appreciation`, `Female College`, `Female Doctor`, `Female Investing`, `Female Teacher`, `Fighting Action`, `Finger Fuck`, `Fisting`, `Footjob`, `Foreign Objects`"
letterG = "`Gal`, `Gangbang`, `Girl`, `Glasses`"
letterH = "`Handjob`, `Hardcore`, `Hostess`, `Hot Spring`, `Huge Butt`, `Huge Cock`, `Humiliation`, `Hypnosis`, `Hentai`"
letterI = "`Idol`, `Image Video`, `Immediate Oral`, `Incest`, `Instructor`"
letterK = "`Kimono`, `Kiss`, `Knee Socks`"
letterL = "`Landlady`, `Leg Fetish`, `Leotard`, `Lesbian`, `Lesbian Kiss`, `Lingerie`, `Lotion`, `Love`"
letterM = "`Maid`, `Married Woman`, `Massage`, `Milf`, `Masturbation`, `Mature Woman`, `Mini`, `Mini Skirt`, `Miss`, `Model`, `Molester`, `Mother`, `Mother-in-law`, `Mourning`, `Multiple Story`, `Muscle`"
letterN = "`Naked Apron`, `Nampa`, `Nasty`, `Nurse`"
letterO = "`OL`, `Older Sister`, `Omnibus`, `Original Collab`, `Other Asian`, `Other Fetish`, `Outdoors`"
letterP = "`POV`, `Pantyhose`, `Piss Drinking`, `Planning`, `Prank`, `Pregnant Woman`, `Promiscuity`, `Prostitutes`"
letterR = "`Race Queen`, `Rape`, `Reserved Role`, `Restraint`, `Restraints`, `Risky Mosaic`"
letterS = "`SM`, `Sailor Suit`, `School Girl`, `School Stuff`, `School Swimsuit`, `School Uniform`, `Secretary`, `Sexy`, `Shaved`, `Shotacon`, `Sister`, `Slave`, `Slender`, `Slut`, `Solowork`, `Sport`, `Squirting`, `Stewardess`, `Subjectivity`, `Submissive Men`, `Sun tan`, `Sweat`, `Swimsuit`"
letterT = "`Tall`, `Tits`, `Titty Fuck`, `Toy`, `Training`, `Transsexual`, `Tsundere`, `Tutor`"
letterU = "`Underwear`, `Uniform`, `Urination`"
letterV = "`Various Profess`, `Vibe`, `Virgin`, `Virgin Man`, `Voyeur`"
letterW = "`Waitress`, `White Actress`, `Widow`"

def INIT_BROWSER():
    chrome1_options = webdriver.ChromeOptions()
    chrome1_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome1_options.add_argument("--headless")
    chrome1_options.add_argument("--disable-dev-shm-usage")
    chrome1_options.add_argument("--no-sandbox")
    chrome1_options.add_argument("--disable-infobars")
    chrome1_options.add_argument("--disable-extensions")
    chrome1_options.add_argument('--disable-application-cache')
    chrome1_options.add_argument('--disable-gpu')
    chrome1_options.add_argument("--disable-dev-shm-usage")
    
    return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options = chrome1_options)
    #return webdriver.Chrome(executable_path="C:\\Users\\admin\\Downloads\\chromedriver_win32\\chromedriver.exe", options = chrome1_options)   

class TripleXsources(commands.Cog):     
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot) 
        
        self.browser1 = INIT_BROWSER()
        self.browser1.get('https://www.r18.com/common/search/image/')
        
        self.browser2 = INIT_BROWSER()
    
    def _ConvertTimestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d/%m/%Y')
    
    def CreateEmbed(self, info):
        date = self._ConvertTimestamp(info['timestamp'])
        show = discord.Embed(title = 'Bạn dùng tới giới hạn của câu lệnh này')
        show.add_field(name = '-----------------------------------------------', value = 'Dưới đây là số lần mà các câu lệnh được sử dụng ở server bạn trong ngày hôm nay. (Sẽ reset lại sau mỗi 24 giờ)', inline = False)
        show.add_field(name = 's.facejp', value = f"`{info['facejp']}/{info['limitFacejpDF']} lần`", inline = True)
        show.add_field(name = 's.faceus', value = f"`{info['faceus']}/{info['limitFaceusDF']} lần`", inline = True)
        show.add_field(name = 's.jav', value = f"`{info['jav']}/{info['limitJavDF']} lần`", inline = True)
        show.add_field(name = 'Thời điểm reset', value = f'`{date}`', inline = False)
        show.add_field(name = 'Nếu có bất kỳ ý kiến gì, xin hãy liên hệ qua server của mình', value = '[Link server](https://discord.gg/27ttfuPAcr)', inline = False)
        return show

    @commands.command(aliases = ['newdebut', 'debut'])
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def NewDebut(self, ctx, date : str = None):
        check = await AllowToUseCommandInThisChannel(ctx, 'debut')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        mess = DebutMess(ctx, LANGUAGE)
        Checkdate = datetime.today()
        
        if date == None:
            month = Checkdate.month
            year = Checkdate.year
        
        else:
            analys = date.split('/')
            if len(analys) != 2:
                await ctx.send(mess[0])
                return
            
            try:
                month = int(analys[0])
                year = int(analys[1])
                
            except ValueError:
                await ctx.send(mess[1])
                return
            
            if (month < 1 or month > 12):
                await ctx.send(mess[2])
                return
            
            if (year < 2020 or year > Checkdate.year):
                await ctx.send(mess[3])
                return
            
            if year == Checkdate.year and month > Checkdate.month:
                await ctx.send(mess[4] + ' `s.debut {Checkdate.month}/{Checkdate.year}`')
                return
        
        find = await AVdebut(month, year)
        if find:
            user = ctx.author
            await ctx.send(mess[5])
            count = 1
            for actor in find:
                show = discord.Embed(title = f"{count}. {actor['actor']}", color = 0x6C3483)
                show.add_field(name = mess[6], value = actor['Date Of Birth'], inline = False)
                show.add_field(name = mess[7], value = actor['Star Sign'], inline = True)
                show.add_field(name = mess[8], value = actor['Place Of Birth'], inline = True)
                show.add_field(name = mess[9], value = actor['Cup'], inline = True)
                show.add_field(name = mess[10], value = actor['Height'] + ' cm', inline = True)
                show.add_field(name = mess[11], value = actor['Measurements'], inline = True)
                show.add_field(name = mess[12], value = actor['Blood Type'], inline = False)
                show.add_field(name = mess[13], value = f'{month}/{year}', inline = True)
                show.add_field(name = 'Debut Code', value = actor['Debut Code'], inline = True)
                show.set_image(url = actor['image'])
                button = Button(style = ButtonStyle.URL, label = f'{actor["Debut Code"]}', url = 'https://www.google.com/search?q=' + actor['Debut Code'], emoji = '🎥')
                await user.send(embed = show, components = [button])
                count += 1
            show1 = discord.Embed(title = f'==> {mess[16]} {count - 1} {mess[17]} {month}/{year}.', color = 0x4EFD00)
            await user.send(embed = show1)
            
        else:
            await ctx.send(mess[14] + f'**{month}/{year}**' + mess[15])
      
    @commands.command(aliases = ['j'])
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def jav(self, ctx, url : str = None):
        """await ctx.send('**Lệnh tạm dừng hoạt động**')
        return"""
    
        check = await checkLimitUsages(ctx.message.guild.id, 'jav', 'limitJavDF')
        if check[0] == False:
            show = self.CreateEmbed(check[1])
            await ctx.send(embed = show)
            return

        #check guild 
        check = await AllowToUseCommandInThisChannel(ctx, 'jav')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        mess = JAVmess(LANGUAGE)
        
        image = getURLimage(url, ctx)
        start = time.time()
        async with ctx.message.channel.typing():
            if image:
                check = CreateImage(image, 'jav.jpg')
                if check:
                    if self.browser1.current_url != 'https://www.r18.com/common/search/image/':
                        self.browser1.get('https://www.r18.com/common/search/image/')
        
                    try:
                        myElem = WebDriverWait(self.browser1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/input')))
                        self.browser1.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/input').send_keys(os.getcwd() + '/jav.jpg')

                        myElem = WebDriverWait(self.browser1, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div[1]')))
                        getData = extract_R18(self.browser1.page_source)

                    except TimeoutException:
                        with open('web.html', 'w+', encoding='utf-8') as f:
                            f.write(str(self.browser1.page_source))
                        await ctx.send(mess[0])

                        channel = self.bot.get_channel(901824213004984360)
                        file = discord.File('web.html', filename = 'web.html')
                        await channel.send(file = file)
                        self.browser1.get('about:blank')

                        return 0

                    if getData:
                        count = 1
                        saveButton = Button(style = ButtonStyle.blue, label = mess[1], emoji = '🎥')
                        
                        for Data in getData:
                            actor = Data["actor"]
                            show = discord.Embed(title = f'{count}. {actor}', color = 0x6C3483)
                            show.add_field(name = mess[2], value = Data['movie_name'], inline = True)
                            show.add_field(name = 'Code', value = Data['code'], inline = True)
                            show.set_image(url = Data['image'])
                            info = await AVinfo(actor)
                            
                            codeButton = Button(style = ButtonStyle.URL, label = f"{Data['code']}", url = 'https://www.google.com/search?q=' + Data['code'] + '%20jav')
                            
                            if actor != "N/A" and info is not None:
                                show.set_thumbnail(url = info['image'])
                                
                                button = Button(style = ButtonStyle.URL, label = actor, url = 'https://www.javdatabase.com/idols/' + actor.replace(' ', '-'), emoji = '❤️')
                                await ctx.send(embed = show, components = [[button, saveButton, codeButton]])

                            else:
                                await ctx.send(embed = show, components = [[saveButton, codeButton]])
                            await ctx.send(Data['trailer'])
                            count += 1
                    
                    else:
                        await ctx.send(mess[0])
                        
                    try:   
                        self.browser1.get('https://www.r18.com/common/search/image/')
                    except:
                        pass
                    
                else:
                    await ctx.send(mess[0])
            else:
                await ctx.send(mess[3])

        end = time.time()
        print(end-start)
        return
        
    @commands.command()
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(per = 1, rate = 60, type = commands.BucketType.default)
    async def faceus(self, ctx, url : str = None):
        check = await checkLimitUsages(ctx.message.guild.id, 'faceus', 'limitFaceusDF')
        if check[0] == False:
            show = self.CreateEmbed(check[1])
            await ctx.send(embed = show)
            return  
        
        check = await AllowToUseCommandInThisChannel(ctx, 'faceus')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        
        mess = FACEmess(LANGUAGE)
        
        image = getURLimage(url, ctx)
        async with ctx.message.channel.typing():
            url = 'https://findpornface.com/searchByPhoto'
            if image:
                self.browser2.get(url)
                self.browser2.find_element_by_xpath('//*[@id="main"]/div/div/div/form/div[2]/input').send_keys(image)
                button = self.browser2.find_element_by_xpath('//*[@id="main"]/div/div/div/form/input')
                
                while url == self.browser2.current_url:
                    button.click()
                      
                try:
                    WebDriverWait(self.browser2, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'searchResultsByPhoto__callToActionWrapper')))
                    
                except TimeoutException:
                    await ctx.send(mess[0])
                    return
                    
                soup = BeautifulSoup(self.browser2.page_source, 'html.parser').find_all('a', class_ = 'actorCompareCard__link', limit = 5)
                for i in soup:
                    baseTEXT = (i.find_all('div', class_ = 'comparePhotos__photo'))[1].attrs['style']
                    
                    name = i.find('h2').text
                    img = re.findall('https://s3.eu-central-1.amazonaws.com/findpornface/preview/+[a-zA-Z0-9_.+-]+\.jpg', baseTEXT)[0]
                    link = 'https://www.babepedia.com/babe/' + name.strip().replace(' ', '_')
                    
                    show = discord.Embed(title = name, colour = 0x6C3483)
                    show.set_image(url = img)
                    button = Button(style = ButtonStyle.URL, label = name + ' bio', url = link, emoji = '❤️')
                    await ctx.send(embed = show, components = [button])
                        
            else:
                await ctx.send(mess[5])
            return                   
                    
    @commands.command(aliases = ['face'])
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(per = 1, rate = 60, type = commands.BucketType.default)
    async def facejp(self, ctx, url : str = None): 
        check = await checkLimitUsages(ctx.message.guild.id, 'facejp', 'limitFacejpDF')
        if check[0] == False:
            show = self.CreateEmbed(check[1])
            await ctx.send(embed = show)
            return

        check = await AllowToUseCommandInThisChannel(ctx, 'facejp')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        mess = FACEmess(LANGUAGE)
        
        image = getURLimage(url, ctx)
        async with ctx.message.channel.typing():
            if image:
                check = CreateImage(image, 'normal.jpg')
                if check:
                    try:
                        self.browser2.get('https://xslist.org/en')
                        myElem = WebDriverWait(self.browser2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu"]/a[3]')))
                        self.browser2.find_element_by_xpath('//*[@id="menu"]/a[3]').click()#

                    except TimeoutException:
                        with open('web.html', 'w+', encoding='utf-8') as f:
                            f.write(str(self.browser2.page_source))

                        channel = self.bot.get_channel(901824213004984360)
                        file = discord.File('web.html', filename = 'web.html')
                        await channel.send(file = file)
                        self.browser2.get('about:blank')

                        await ctx.send(mess[0])
                        return 0

                    self.browser2.find_element_by_xpath('//*[@id="pic-submit-input"]').send_keys(os.getcwd() + '/normal.jpg')
                    try:
                        myElem = WebDriverWait(self.browser2, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/ul/li[1]')))
                    except TimeoutException:
                        await ctx.send(mess[0])
                        return 0

                    await asyncio.sleep(0.5)
                    try:
                        data = extract_Xlist(str(self.browser2.page_source))
                    except:
                        await ctx.send(mess[0])
                        return
                    
                    saveInfo = Button(style = ButtonStyle.green, label = mess[1], emoji = '🤸‍♀️')
                    for info in data:
                        show = discord.Embed(title = info['actor'], description = f'{mess[2]} {info["similar"]}', color = 0x6C3483)
                        show.add_field(name = 'Cup', value = info['cup'], inline = True)
                        show.add_field(name = mess[3], value = info['height'], inline = True)
                        show.add_field(name = mess[4], value = info['measurements'], inline = False)
                        show.set_thumbnail(url = info['avatar'])

                        button = Button(style = ButtonStyle.URL, label = info['actor'] + ' bio', url = 'https://www.javdatabase.com/idols/' + info['actor'].replace(' ', '-'), emoji = '❤️')
                        await ctx.send(embed = show, components = [[button, saveInfo]])
                        
            else:
                await ctx.send(mess[5])
            return
                    
    @commands.command(aliases = ['code'])
    @commands.guild_only()
    @commands.is_nsfw()
    @commands.cooldown(1, 2, commands.BucketType.guild)
    async def CodeJAV(self, ctx, *, tag : str = ''):   
        check = await AllowToUseCommandInThisChannel(ctx, 'code')
        LANGUAGE = await getLanguage(ctx.message.guild.id)
        
        if not check[0]:
            mess = ''
            for id in check[1]:
                channel = self.bot.get_channel(id)
                mess += f'{channel.mention} '
                
            await ctx.send(AllowToUseCommand(LANGUAGE) + mess)
            return
        mess = RandomMovieMess(LANGUAGE)
        
        tag = tag.lower().strip()
           
        if tag == 'tag' or tag == 'tags':
            show = discord.Embed(title = 'TAGS', color = 0x6C3483)
            show.add_field(name = 'Number', value = letterNum, inline = False)
            show.add_field(name = 'A', value = letterA, inline = False)
            show.add_field(name = 'B', value = letterB, inline = False)
            show.add_field(name = 'C', value = letterC, inline = False)
            show.add_field(name = 'D', value = letterD, inline = False)
            show.add_field(name = 'E', value = letterE, inline = False)
            show.add_field(name = 'F', value = letterF, inline = False)
            show.add_field(name = 'G', value = letterG, inline = False)
            show.add_field(name = 'H', value = letterH, inline = False)
            show.add_field(name = 'I', value = letterI, inline = False)
            show.add_field(name = 'K', value = letterK, inline = False)
            show.add_field(name = 'L', value = letterL, inline = False)
            show.add_field(name = 'M', value = letterM, inline = False)
            show.add_field(name = 'N', value = letterN, inline = False)
            show.add_field(name = 'O', value = letterO, inline = False)
            show.add_field(name = 'P', value = letterP, inline = False)
            show.add_field(name = 'R', value = letterR, inline = False)
            show.add_field(name = 'S', value = letterS, inline = False)
            show.add_field(name = 'T', value = letterT, inline = False)
            show.add_field(name = 'U', value = letterU, inline = False)
            show.add_field(name = 'V', value = letterV, inline = False)
            show.add_field(name = 'W', value = letterW, inline = False)
            await ctx.send(embed = show)
            return
        
        code_JAV = db.getCollection('JAVcode')
        if tag == '':
            getJAVINFO = code_JAV.aggregate([{'$match' : {}}, {"$sample": { "size": 3 }}])
            
        else:
            getJAVINFO = code_JAV.aggregate([{'$match' : {'tag' : {'$regex' : tag}}}, {"$sample": { "size": 3 }}])
        
        check = False
        saveButton = Button(style = ButtonStyle.blue, label = mess[0], emoji = '🎥')
        for data in getJAVINFO:
            check = True
            show = discord.Embed(description = ", ".join([f'`{av}`' for av in data['av'].split(':')]), color = 0x6C3483)
            show.add_field(name = mess[1], value = data['duration'], inline = True)
            show.add_field(name = 'Code', value = data['code'], inline = True)
            show.add_field(name = 'Tag', value = " - ".join([f'`{tag}`' for tag in data['tag'].split(':')]), inline = False)
            show.set_image(url = data['image'])
            
            if '-' in data['code']:
                button = Button(style = ButtonStyle.URL, label = data["code"], url = f'https://www.google.com/search?q={data["code"]}+jav')
            else:
                button = Button(style = ButtonStyle.URL, label = data["code"], url = f"https://www.google.com/search?q={quote(data['title'])}")
            
            await ctx.send(embed = show, components = [[saveButton, button]])
            await ctx.send(data['trailer'])

            
        if check == False:
            await ctx.send(mess[2])
                  
                
def setup(bot):
    bot.add_cog(TripleXsources(bot))