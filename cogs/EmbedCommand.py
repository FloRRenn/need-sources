from tkinter.tix import Tree
import discord

def SetupEmbed(lang : str = 'vi'):
    if lang == 'vi':
        setup = discord.Embed(title = '🛠️ Setup 🛠️', description = '**Chỉ admin hoặc người có quyền hạn tương đương mới được sử dụng các lệnh trong đây**', color = 0xDEFC01)
        setup.add_field(name = '1. Tùy chỉnh lệnh được phép dùng trong kênh', value = '`s.setup <lệnh 1>,<lệnh 2>,...`\n```- Cách dùng: Sử dụng lệnh này trong chính kênh muốn **đặt** ràng buộc.\n- Giải thích: Khi sử dụng lệnh này, bạn chỉ cho phép member sử dụng lệnh (<lệnh 1>, <lệnh 2>,..) trong kênh bạn cho phép.\n- Ví dụ: Khi bạn dùng "s.setup a" trong kênh `A` thì lệnh "s.a" chỉ được phép dùng trong kênh `A`, **bot** sẽ từ chối thực hiện yêu cầu nếu lệnh được sử dụng trong kênh khác.```', inline = False)
        setup.add_field(name = '2. Xóa ràng buộc sử dụng lệnh trong kênh', value = '`s.drop <lệnh>`\n```- Cách dùng: Sử dụng lệnh này trong chính kênh muốn **xóa** ràng buộc.\n- Giải thích: Khi sử dụng lệnh này, câu lệnh mà bạn đã ràng buộc cho kênh từ trước sẽ bị xóa.\n- Ví dụ: Nếu trước kia, lệnh "s.a" chỉ có thể được sử dụng trong kênh `A`, khi bạn dùng lệnh "s.drop a" thì câu lệnh `s.a` được phép sử dụng trong tất cả kênh của bạn.```', inline = False)
        setup.add_field(name = '3. Xem các kênh bị ràng buộc sử dụng lệnh', value = '`s.manage`', inline = False)
        setup.add_field(name = '4. Chọn ngôn ngữ hiển thị', value = '`s.lang en/vi`', inline = False)
        setup.add_field(name = '- - - - - - - - - - - - - - -', value = '__Tên các lệnh__', inline = False)
        setup.add_field(name = 'Tìm nguồn', value = '`anime` `src`', inline = True)
        setup.add_field(name = 'Tìm Người', value = '`facejp` `faceus`', inline = True)
        setup.add_field(name = 'Tìm code', value = '`jav` `code`', inline = True)
        setup.add_field(name = 'Ảnh SFW', value = '`waifu` `booru` `danbooru` `gelbooru` `konachan` `yandere`', inline = True)
        setup.add_field(name = 'Ảnh NSFW', value = '`nwaifu` `nbooru` `ndanbooru` `ngelbooru` `nkonachan` `nyandere` `rule34` `debut` `henbyid` `henbytag`', inline = True)
        setup.add_field(name = 'Khác', value = '`quote`', inline = True)
                    
    else:
        setup = discord.Embed(title = '🛠️ Setup 🛠️', description = '**Just the admin can use these commands below**`', color = 0xDEFC01)
        setup.add_field(name = '1. Allow to use specified commands in channel', value = '`s.setup <name of command 1>,<name of command 2>,...`\n- Usage: Just allow member uses any commands that you want in specified channels. Use this command with name of command that you want in specified channel, then bot auto setup for you.\nFor example: You use `s.setup anime,src` in channel __A__, so command `anime` and `src` can not be used in other channel except channel __A__', inline = False)
        setup.add_field(name = '2. Delete constraint', value = '`s.drop <name of command>``\n- Usage: If you use `s.setup`, then you change your mind and want to delete this setup, this command will help you to do that', inline = False)
        setup.add_field(name = '3. See all setup in every channel', value = '`s.manage`', inline = False)
        setup.add_field(name = '4. Choose language', value = '`s.lang en/vi`', inline = False)
        setup.add_field(name = '- - - - - - - - - - - - - - -', value = '__Command name__', inline = False)
        setup.add_field(name = 'Find source', value = '`anime` `src`', inline = True)
        setup.add_field(name = 'Find person', value = '`facejp` `faceus`', inline = True)
        setup.add_field(name = 'Find code', value = '`jav` `code`', inline = True)
        setup.add_field(name = 'SFW image', value = '`waifu` `booru` `danbooru` `gelbooru` `konachan` `yandere`', inline = True)
        setup.add_field(name = 'NSFW image', value = '`nwaifu` `nbooru` `ndanbooru` `ngelbooru` `nkonachan` `nyandere` `rule34` `debut` `henbyid` `henbytag`', inline = True)
        setup.add_field(name = 'Other', value = '`quote`', inline = True)
    return setup
        
def SourceEmbed(lang : str = 'vi'):
    if lang == 'vi':
        source = discord.Embed(title = "🔎 Tìm nguồn🔎", color = 0x6C3483)
        #source.add_field(name = 'Tìm linh tinh', value = '```s.src <link_ảnh/ảnh_từ_thiết_bị>```', inline = False)
        source.add_field(name = '1. Tìm nguồn Anime/Artwork', value = '```s.a ảnh/video```', inline = True)
        source.add_field(name = '2. Tìm code JAV', value = '```s.jav ảnh```\n__Thời gian tìm kiếm có thể mất vài giây__', inline = False)
        source.set_thumbnail(url = 'https://i.imgur.com/tCmkJtM.jpg')
        
    else:
        source = discord.Embed(title = "🔎 Find Source🔎", color = 0x6C3483)
        #source.add_field(name = 'Tìm linh tinh', value = '```s.src <link_ảnh/ảnh_từ_thiết_bị>```', inline = False)
        source.add_field(name = '1. Source of Anime/Artwork', value = '```s.a image/video```', inline = True)
        source.add_field(name = '2. Find code JAV', value = '```s.jav image```\n__It will take a few minutes to respond a result__', inline = False)
        source.set_thumbnail(url = 'https://i.imgur.com/tCmkJtM.jpg')
    return source

def FaceEmbed(lang : str = 'vi'):
    if lang == 'vi':
        facedetect = discord.Embed(title = '🕵🏻‍♂️ Nhận diện khuôn mặt (Face Detection) 🕵🏻‍♂️', color = 0x2980B9)
        facedetect.add_field(name = '1. Nhận diện diễn viên JAV', value = '```s.facejp ảnh```', inline = False)
        facedetect.add_field(name = '2. Nhận diện diễn viên US-UK', value = '```s.faceus ảnh```\n__Thời gian tìm kiếm có thể mất vài giây__', inline = False)
        facedetect.set_thumbnail(url = 'https://i.imgur.com/h6pqfRT.jpg')
        
    else:
        facedetect = discord.Embed(title = '🕵🏻‍♂️ Face Recognition 🕵🏻‍♂️', color = 0x2980B9)
        facedetect.add_field(name = '1. JAV actress', value = '```s.facejp image```', inline = False)
        facedetect.add_field(name = '2. US-UK actress', value = '```s.faceus image```\n__It will take a few minutes to respond a result__', inline = False)
        facedetect.set_thumbnail(url = 'https://i.imgur.com/h6pqfRT.jpg')
    return facedetect

def WaifuEmbed(lang : str = 'vi'):
    if lang == 'vi':
        waifu = discord.Embed(title = '🔥 Random art/anime image 🔥', description = '__Cách dùng__: **lệnh + tên_tag_hoặc_bỏ_trống**\n```Ví dụ: s.booru genshin_impact```', color = 0xF39C12)
        waifu.add_field(name = '1. SFW waifu', value = "`s.waifu`", inline = True)
        waifu.add_field(name = '2. NSFW waifu', value = "`s.nwaifu`", inline = True)
        waifu.add_field(name = '3. Ảnh random từ Rule34 ', value = '`s.r34`', inline = False)
        waifu.add_field(name = '4. SFW Booru', value = '`s.booru`\n`s.dan`\n`s.gel`\n`s.kona`\n`s.yan`', inline = True)
        waifu.add_field(name = '5. NSFW Booru', value = '`s.nbooru`\n`s.ndan`\n`s.ngel`\n`s.nkona`\n`s.nyandere`', inline = True)
        waifu.set_thumbnail(url = 'https://i.imgur.com/XWr5JB9.jpg')
        
    else:
        waifu = discord.Embed(title = '🔥 Random art/image 🔥', description = ' __Usage__: **command + tag_name_or_not**\n```Example: s.booru genshin_impact```', color = 0xF39C12)
        waifu.add_field(name = '1. SFW waifu', value = "`s.waifu`", inline = True)
        waifu.add_field(name = '2. NSFW waifu', value = "`s.nwaifu`", inline = True)
        waifu.add_field(name = '3. Random pictures from Rule34 ', value = '`s.r34`', inline = False)
        waifu.add_field(name = '4. SFW Booru', value = '`s.booru`\n`s.dan`\n`s.gel`\n`s.kona`\n`s.yan`', inline = True)
        waifu.add_field(name = '5. NSFW Booru', value = '`s.nbooru`\n`s.ndan`\n`s.ngel`\n`s.nkona`\n`s.nyan`', inline = True)
        waifu.set_thumbnail(url = 'https://i.imgur.com/XWr5JB9.jpg')
        
    return waifu
  
def OtherEmbed(lang : str = 'vi'):  
    if lang == 'vi':
        other = discord.Embed(title = '🤔 Khác 🤔', color = 0x16A085)
        other.add_field(name = '1. Xem diễn viên mới debut trong tháng', value = '`s.debut <mm/yyyy> (định dạng nhập tháng/năm)` hoặc `s.debut (xem trong tháng này)`', inline = False)
        other.add_field(name = '2. Random JAV Code', value = '`s.code <tag>` hoặc `s.code`\nXem các **tag** có thể sử dụng: `s.code tag`', inline = False)
        other.add_field(name = '3. Câu nói hay từ một bộ anime nào đó', value = '```s.quote```', inline = False)
        #other.add_field(name = '4. Mời tui vào server của bạn', value = '```s.inv```', inline = False)
        other.add_field(name = '4. Tạo card', value = '`s.card`', inline = False)
        other.set_thumbnail(url = 'https://i.imgur.com/cgmxetk.jpg')
        
    else:
        other = discord.Embed(title = '🤔 Other 🤔', color = 0x16A085)
        other.add_field(name = '1. See new debut actresses in this month', value = '`s.debut mm/yyyy (month/year)` or `s.debut` (see in this month)', inline = False)
        other.add_field(name = '2. Random JAV Code', value = '`s.code <tag>` or `s.code (random tag)`\nTo see more available tags, type `s.code tag`', inline = False)
        other.add_field(name = '3. Random quote in random anime', value = '`s.quote`', inline = False)
        other.add_field(name = '4. Create custom card', value = '`s.card`', inline = False)
        #other.add_field(name = '4. Mời tui vào server của bạn', value = '```s.inv```', inline = False)
        other.set_thumbnail(url = 'https://i.imgur.com/cgmxetk.jpg')
        
    return other

def HentaiEmbed(lang : str = 'vi'):
    if lang == 'vi':
        hen = discord.Embed(title = '😶 Hen 😶', description = 'Đọc truyện từ **nhentai.net**', colour = 0xFC01BB)
        hen.add_field(name = '1. Đọc truyện từ ID', value = '`s.henid ID`', inline = False)
        hen.add_field(name = '2. Đọc truyện từ tag', value = '`s.hentag tag`', inline = False)
        hen.set_thumbnail(url = 'https://i.imgur.com/61TRjEI.jpg')
        
    else:
        hen = discord.Embed(title = '😶 Hen 😶', description = 'Read doujin from **nhentai.net**', colour = 0xFC01BB)
        hen.add_field(name = '1. Read by ID', value = '`s.henid ID`', inline = False)
        hen.add_field(name = '2. Read by tag', value = '`s.hentag tag`', inline = False)
        hen.set_thumbnail(url = 'https://i.imgur.com/61TRjEI.jpg')
    return hen

def JustADMIN(lang : str = 'vi'):
    if lang == 'vi':
        return '**Chỉ admin hoặc người có quyền hạn tương đương mới có thể xem nội dung bên trong.**'
    return '**Just admin see these commands in here**'

def HelpEmbed(lang : str = 'vi'):
    if lang == 'vi':
        title = '⬇️ Bấm vào `Commands` để xem lệnh ⬇️'
        description = 'Tau có sources - Bảng trợ giúp'
        
        source = 'Tìm nguồn'
        face = 'Tìm người'
        entertaint = 'Giải trí'
        other = 'Khác'
        
    else:
        title = '⬇️ Click on `Commands` to see the list of commands ⬇️'
        description = 'Tau có sources - Help board'
        
        source = 'Find source'
        face = 'Find person'
        entertaint = 'Entertaintment'
        other = 'Other'
        
    return (title, description, source, face, other, entertaint)