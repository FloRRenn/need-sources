from .saucenao_api import SauceNao, LongLimitReachedError, ShortLimitReachedError, UnknownClientError
from re import search
from requests import get
from bs4 import BeautifulSoup
from .Language import SourceError, InputImageError
from cv2 import VideoCapture, imwrite
from discord import File
from .TextWraper import shorten

headerImage = {
                'dnt': '1',
                'sec-ch-ua': '" Not;A Brand";v="99", "CocCoc";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/97.0.194 Chrome/91.0.4472.194 Safari/537.36'
            }

headerYandex = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5,zh-CN;q=0.4,zh;q=0.3,ja;q=0.2',
                'cache-control': 'max-age=0',
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


def YandexCrawl(url, cookie : str):
    getSiteIfURLHaveThis = ['sankakucomplex.com', 'safebooru.org', 'danbooru.donmai.us', 'gelbooru.com', 'yande.re' , 'zerochan.net', 'realbooru.com', 'konachan.net', "hentai", 'rule34.']

    header = {
        **headerYandex,
        'cookie' : cookie
    }
    
    try:
        resp = get(url, headers = header)     
        soup = BeautifulSoup(resp.content, 'html.parser').find_all('div', class_ = 'CbirSites-Item', limit = 20)
        
        for data in soup:
            urlDest = data.find('div', class_ = 'CbirSites-ItemTitle').find('a').attrs['href']
            img = data.find('div', class_ = 'CbirSites-ItemThumb').find('a').attrs['href']
            info = {
                'url' : urlDest,
                'thumb' : img
            }
            
            if any(word in urlDest for word in getSiteIfURLHaveThis):
                return info
            
        index = min(2, len(soup)) - 1
        info = {
                'url' : soup[index].find('div', class_ = 'CbirSites-ItemTitle').find('a').attrs['href'],
                'thumb' : soup[index].find('div', class_ = 'CbirSites-ItemThumb').find('a').attrs['href']
            }
        return info
    
    except Exception as e:
        return None

def getURL(fromTEXT : str, fromATTACHMENT):
    url = None
        
    try:  
        if len(fromATTACHMENT) > 0:
            url = fromATTACHMENT[0].url
            
        elif fromTEXT is not None and url is None:
            try:
                url = search("(?P<url>https?://[^\s]+)", fromTEXT).group("url")
            except:
                pass
    except:
        pass
    return url 

def readFirstFrame(url):
    vidcap = VideoCapture(url)
    success,image = vidcap.read()
    count = 0
    while success:
        success,image = vidcap.read()
        if count == 10:
            imwrite("frame.jpg", image)  
            break
        count += 1  
            
def downloadVideo(response, type : str):
    with open(f'test.{type}', 'wb') as f:
        for chunk in response.iter_content(chunk_size = 1024):
            if chunk:
                f.write(chunk)
                f.flush()
    readFirstFrame(type)

async def is_image_or_video(url, image_name : str, lang : str = 'vi'):
    image_formats = "image/"
    video_formats = "video/"
    try:
        resp = get(url, headers = headerImage, stream=True, timeout = 10)
        size = int(resp.headers['content-length'])/(1024**2)
        
    except:
        code = 3 #cant connect to this url
        mess = SourceError(code, lang)
        return code, mess
    
    content_type = resp.headers['content-type']
    try:
        if resp.status_code == 200:
            if content_type.startswith(video_formats):
                if size <= 40:
                    readFirstFrame(url)
                    return 50, 'Is Video'
                else:
                    code = 2 #size > 10
                    mess = SourceError(code, lang)
            
            elif content_type.startswith(image_formats):
                if size < 20:
                    return 60, 'Is Image'
                else:
                    code = 2 #size > 10
                    mess = SourceError(code, lang)

            else:
                code = 1 #wrong format
                mess = SourceError(code, lang)
                
        else:
            code = 3 #cant connect to this url
            mess = SourceError(code, lang)
    except:
        code = 3 #cant connect to this url
        mess = SourceError(code, lang)
        
    return code, mess

async def getHistoryMess(ctx):
    count = 0
    async for message in ctx.channel.history(limit = 5):
        if message.author == ctx.author:
            if message.content.startswith('https') or len(message.attachments) > 0:
                return getURL(message.content, message.attachments)      
    return None           

async def FindSauce(bot, ctx, api, fromTEXT, fromATTACHMENT, lang : str = 'vi'):
    if fromTEXT is None and len(fromATTACHMENT) == 0:
        url = await getHistoryMess(ctx)
        
    else:
        url = getURL(fromTEXT, fromATTACHMENT)    
        
    code = 0
    if url != None:
        code, resp = await is_image_or_video(url, 'frame.jpg', lang)
        try:
            if code == 50:
                sauce = SauceNao(api)
                with open('frame.jpg', 'rb') as f:
                    res = sauce.from_file(f)
                data = res[0].raw

                if float(data['header']['similarity']) < 60:  
                    channel = bot.get_channel(930659053095497768)
                    with open('frame.jpg', 'rb') as f:
                        picture = File(f)
                        msg = await channel.send(file = picture) 
                    url = msg.attachments[0].url
                    
                return (code, data, url)
            
            elif code == 60:
                sauce = SauceNao(api)
                res = sauce.from_url(url)
                return (code, res[0].raw, url)
            
            else:
                return (code, resp, "")
            
        except LongLimitReachedError:
            return (0, '**Server của bạn đã dùng hết lượt cho ngày hôm nay. Vui lòng thử lại sau.**', "")
        
        except ShortLimitReachedError:
            return (0, 'Vui lòng thử lại sau **30 giây** nữa.', "")
            
        except Exception as e:
            channel = bot.get_channel(909404622278520872)
            await channel.send(shorten(str(e), width = 4000))
            
            if code == 60:
                """if count < 2:
                    api = 'd18a27bcfcd4692bc467a312fc60734b9157f241'
                    count += 1 
                
                else:"""
                return (61, '', url)
            
            elif code == 50:
                """if count < 2:
                    api = 'd18a27bcfcd4692bc467a312fc60734b9157f241'
                    count += 1 
                else:"""
                return (51, '', url)
            
            else:
                return (code, resp, "")
    
    mess = InputImageError(lang)
    return (0, mess, '')

async def get_any_url(bot, fromTEXT, fromATTACHMENT, lang):
    url = getURL(fromTEXT, fromATTACHMENT)
    
    if url != None:
        code, resp = await is_image_or_video(url, 'frame.jpg', lang)
        
        if code == 50:
            channel = bot.get_channel(930659053095497768)
            with open('frame.jpg', 'rb') as f:
                picture = File(f)
                msg = await channel.send(file = picture) 
            url = msg.attachments[0].url
            
            #saafsafasfddddassfdasdads
            