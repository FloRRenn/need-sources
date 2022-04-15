from discord.ext import commands
from discord.ext.commands.core import guild_only
from discord_components import *
from discord import File, Embed

from PIL import Image, ImageFilter, ImageFont, ImageEnhance, ImageSequence, ImageOps, ImageColor
from requests import get as connect_to
#from .Ultils.TextWraper import fill
import qrcode, openpyxl
from pilmoji import Pilmoji

class CreateCard(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        DiscordComponents(bot)
        
    def downloadExcel(self, url : str):
        resp = connect_to(url, stream = True, timeout = 60)
        if resp.headers['Content-Type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            with open('data.xlsx', 'wb') as output:
                output.write(resp.content)
            return True
        return False
            
    def download_image(self, image_url : str, filename : str):
        non_gif = ['image/jpeg', 'image/png', 'image/webp']
        gif = ['image/gif']
        
        try:
            response = connect_to(image_url, stream = True, timeout = 60)
        except Exception:
            return '305'
        
        if response.status_code == 200:
            content_type = response.headers['Content-Type']
            size = round(int(response.headers['Content-Length']) / (1024 ** 2))
            if size > 15:
                return '430'
            type = ''
            
            if content_type in non_gif:
                type = '.png'
                with open(filename + type, 'wb') as f:
                    f.write(response.content)
                return filename + type
            
            elif content_type in gif:
                if filename == 'avatar':
                    return '404'
                type = '.gif'
                    
                with open(filename + type, 'wb') as f:
                    f.write(response.content)
                return filename + type
            
        return '305' 
    
    def get_dominant_color(self, pil_img, palette_size : int):
        # Resize image to speed up processing
        img = pil_img.copy()
        img.thumbnail((100, 100))

        # Reduce colors (uses k-means internally)
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

        # Find the color that occurs most often
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)
        palette_index = color_counts[0][1]
        dominant_color = tuple(palette[palette_index*3:palette_index*3+3])

        return dominant_color
    
    def get_color_map(self, hex_color):
        hex_color_index = [
            (255, 255, 255), #white
            (0, 0, 0), #black
            (211, 211, 211), #light gray
            (102, 153, 204), #blue gray
            (133, 193, 233), #dark blue
            (243, 156, 18), #orange
            (127, 140, 141), #gray
            (255, 215, 0), #gold
            (46, 134, 193), #light blue
            (39, 174, 96) #green
        ]

        try:
            RGB = ImageColor.getrgb(f'#{hex_color}')
            if len(RGB) == 4:
                RGB = RGB[1:]
        except ValueError:
            RGB = hex_color_index[hex_color] 
        return RGB
    
    
    def get_first_frame(self, image : Image):
        for frame in ImageSequence.Iterator(image):
            return frame
    
    @commands.guild_only()
    @commands.command(aliases = ['card'])
    #@commands.cooldown(2, 120, commands.BucketType.user)
    async def create_card(self, ctx):
        excel_file = ctx.message.attachments
        
        if len(excel_file) == 0:
            wb = openpyxl.load_workbook('info.xlsx')
            worksheet = wb['Sheet1']
            worksheet['B1'].value = ctx.author.name
            worksheet['B4'].value = f'#{ctx.author.discriminator}'
            worksheet['B7'].value = 'https://cdn.discordapp.com/avatars/' + str(ctx.author.id) + '/' + str(ctx.author.avatar) + '.png'
            wb.save('info.xlsx')
            wb.close()
            
            show = Embed(title = 'Create your custom card', colour = 0x00FF6C)
            show.set_image(url = 'https://i.imgur.com/VH3oKan.gif')
            await ctx.send(embed = show)
            
            file = File('./info.xlsx')
            await ctx.send(file = file)
            await ctx.send('Hãy điền thông tin vào file `info.xlsx` phía trên và gửi lại như hình \nhttps://i.imgur.com/MKx6M6N.png')
            
        else:
            async with ctx.message.channel.typing():
                mess = await ctx.send('Đang thu thập thông tin...')
                
                if not excel_file[0].filename.endswith('.xlsx') and not excel_file[0].filename.endswith('.xls'):
                    await mess.edit('Vui lòng gửi **1 file excel** như hình \nhttps://i.imgur.com/MKx6M6N.png')
                    return
                
                download_excel = self.downloadExcel(excel_file[0].url)
                if download_excel == False:
                    await mess.edit('Vui lòng gửi **1 file excel** như hình \nhttps://i.imgur.com/MKx6M6N.png')
                    return
                    
                try:
                    wb = openpyxl.load_workbook('data.xlsx')
                except:
                    await mess.edit('**Đây không phải là file excel**')
                    return
                
                worksheet = wb.active
                
                info = {
                    'background_url' : str(worksheet['B8'].value),
                    'avatar_url': str(worksheet['B7'].value),
                    'QRcode' : worksheet['B14'].value,
                    'username' : str(worksheet['B1'].value),
                    'discriminator' : str(worksheet['B4'].value),
                    'small_description' : str(worksheet['B11'].value) if worksheet['B11'].value else '',
                    'nitro' : worksheet['B16'].value,
                    'username_color' : self.get_color_map(worksheet['B2'].fill.start_color.index),
                    'discriminator_color' : self.get_color_map(worksheet['B5'].fill.start_color.index),
                    'background_color' : self.get_color_map(worksheet['B9'].fill.start_color.index),
                    'small_description_color' : self.get_color_map(worksheet['B12'].fill.start_color.index)
                }
                wb.close()
                
                await mess.edit('Đang tải ảnh background...')
                background_image = self.download_image(info['background_url'], 'background')
                if background_image == '305':
                    await mess.edit('Link ảnh **background** không thể truy cập được, vui lòng sử dụng 1 link khác')
                    return
                
                elif background_image == '430':
                    await mess.edit('Dung lượng ảnh **background** quá lớn `(> 15mb)`')
                    return
                
                await mess.edit('Đang tải ảnh avatar...')
                avatar_image = self.download_image(info['avatar_url'], 'avatar')
                if avatar_image == '404':
                    await mess.edit('Ảnh avatar không được là ảnh GIF')
                    return
                
                elif avatar_image == '305':
                    await mess.edit('Link ảnh **avatar** không thể truy cập được, vui lòng sử dụng 1 link khác')
                    return
                
                elif avatar_image == '430':
                    await mess.edit('Dung lượng ảnh **avatar** quá lớn `(> 15mb)`')
                    return
                
                await mess.edit('Đang xử lý thông tin...')
                
                theme_material = Image.open(background_image)
                if background_image.endswith('.png'):
                    theme = theme_material.copy()
                    new_size = (960, int(theme_material.height * (960/theme_material.width)))
                    theme = theme.resize(new_size, Image.ANTIALIAS)
                    theme = ImageOps.fit(theme, (theme.width, 350), Image.ANTIALIAS)#theme.crop((0, 0, theme.width, 350))
                    
                    if info['background_color'] == (0,0,0):
                        main_color = self.get_dominant_color(theme, 20)
                    else:
                        main_color = info['background_color']
                    background = Image.new('RGBA', (960, 400), main_color)

                    username_length = 0
                    with Pilmoji(background) as pilmoji:
                        #add username
                        font = ImageFont.truetype(r'./card/fonts/TCCEB.TTF', 35)
                        pilmoji.text((220, 265), info['username'], info['username_color'], font = font)
                        username_length = font.getsize(info['username'])[0]
                        
                        pilmoji.text((220 + font.getsize(info['username'])[0], 265), info['discriminator'], info['discriminator_color'], font = font)
                        username_length += font.getsize(info['discriminator'])[0]
                        
                        #add small description
                        font = ImageFont.truetype(r'./card/fonts/TCCEB.TTF', 20)
                        #small_description = fill(small_description, width = 90, replace_whitespace = True, fix_sentence_endings = True)
                        pilmoji.text((220, 300), info['small_description'], info['small_description_color'], font = font)
                    
                    #QR code
                    if info['QRcode'] != None:
                        qr_img = qrcode.make(info['QRcode'], box_size = 3, border = 1)
                        qr_img = qr_img.resize((80, 80))
                        
                        if username_length > 539:
                            background.paste(qr_img, (770, 305))
                        else:
                            background.paste(qr_img, (770, 290))
                            
                    #add nitro
                    if info['nitro'] == True:
                        booster_mask = Image.open(r'./card/materials/nitro_mask.jpg').convert('L')
                        booster = Image.open(r'./card/materials/nitro.jpg')

                    #create shadow and avatar
                    avatar_mask = shadow_material = Image.open(r'./card/materials/small_avatar_mask.jpg').convert('L')
                    theme_mask = Image.open(r'./card/materials/theme_mask.png')

                    shadow = shadow_material.filter(ImageFilter.GaussianBlur(radius = 3))
                    shadow = ImageEnhance.Brightness(shadow)
                    shadow = shadow.enhance(0.5)

                    avatar_material = Image.open(avatar_image).convert('RGBA')
                    if avatar_material.height != avatar_material.width:
                        avatar = ImageOps.fit(avatar_material, (150, 150), Image.ANTIALIAS)
                    else:
                        avatar = avatar_material.resize((150,150), Image.ANTIALIAS)
                    
                    #paste images onto background  
                    background.paste(theme, (0,0), theme_mask)
                    background.paste(shadow, (60, 220), shadow)
                    background.paste(avatar, (60, 220), avatar_mask)
                    
                    if info['nitro'] == True:
                        background.paste(booster, (800, 215), booster_mask)

                    background.save('result.png', quality = 100)
                    file = File('result.png')
                    
                else:
                    if info['background_color'] == (0,0,0):
                        img = self.get_first_frame(theme_material)
                        main_color = self.get_dominant_color(img, 20)#(24,25,28)#
                    else:
                        main_color = info['background_color']
                    background = Image.new('RGBA', (1200, 500), main_color).convert('RGBA')

                    username_length = 0
                    with Pilmoji(background) as pilmoji:
                        #add username
                        font = ImageFont.truetype(r'./card/fonts/TCCEB.TTF', 44)
                        pilmoji.text((320, 310), info['username'], info['username_color'], font = font)
                        username_length = font.getsize(info['username'])[0]
                        
                        pilmoji.text((320 + username_length, 310), info['discriminator'], info['discriminator_color'], font = font)
                        username_length += font.getsize(info['discriminator'])[0]
                        
                        #add small description
                        font = ImageFont.truetype(r'./card/fonts/TCCEB.TTF', 30)
                        #small_description = fill(small_description, width = 90, replace_whitespace = True, fix_sentence_endings = True)
                        pilmoji.text((320, 355), info['small_description'], info['small_description_color'], font = font)
                        
                    #add nitro
                    booster_mask = Image.open(r'./card/materials/nitro_mask.jpg').convert('L')
                    booster = Image.open(r'./card/materials/nitro.jpg')
                    
                    #resize QR code 
                    if info['QRcode'] != None:
                        qr_img = qrcode.make(info['QRcode'], box_size = 3, border = 1)
                        qr_img = qr_img.resize((95,95))
                        
                        if username_length > 576:
                            background.paste(qr_img, (970, 360))
                        else:
                            background.paste(qr_img, (970, 340))
                    
                    #create shadow for avatar
                    avatar_mask = shadow_material = Image.open(r'./card/materials/avatar_mask.jpg').convert('L')
                    avatar_mask = avatar_mask.resize((220,220), Image.NEAREST)
                    
                    shadow = shadow_material.filter(ImageFilter.GaussianBlur(radius = 3))
                    shadow = ImageEnhance.Brightness(shadow)
                    shadow = shadow.enhance(0.5)

                    avatar_material = Image.open(avatar_image).convert('RGBA')
                    if avatar_material.height != avatar_material.width:
                        avatar = ImageOps.fit(avatar_material, (220,220), Image.ANTIALIAS)
                    else:
                        avatar = avatar_material.resize((220,220), Image.ANTIALIAS)

                    #get background
                    theme_mask = Image.open(r'./card/materials/theme_mask.png')
                    theme_frames = []
                    for frame in ImageSequence.Iterator(theme_material):
                        image = background.copy()
                        new_size = (1200, int(frame.height * (1200/ frame.width)))
                        theme = frame.resize(new_size, Image.NEAREST)
                        theme = ImageOps.fit(theme, (1200, 310), Image.ANTIALIAS)
                        theme.convert('RGBA')
                        
                        image.paste(theme, (0,0))
                        if info['nitro'] == True:
                            image.paste(booster, (1050, 270), booster_mask)
                            
                        image.paste(shadow, (88, 220), shadow)
                        image.paste(avatar, (88, 220), avatar_mask)
                            
                        theme_frames.append(image)
                        
                    theme_frames[0].save('result.gif', save_all = True, append_images = theme_frames[1:], loop = 10)
                    file = File('result.gif')
                    
                await mess.edit('Kết quả')
                mess = await ctx.send(file = file)
                await ctx.send('Hãy cho tui biết bạn có hài lòng với ảnh trên hay không bằng cách sử dụng\n```s.feedback đánh_giá```')
                
                channel = self.bot.get_channel(909404622278520872)
                await channel.send(f'__{ctx.author}__ đã sử dụng s.card ở sever `{ctx.message.guild.name}` - kênh `{ctx.message.channel.name}`')
                            
def setup(bot):
    bot.add_cog(CreateCard(bot))