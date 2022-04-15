from .Sauce import headerImage
from requests import get
from PIL import Image
from bs4 import BeautifulSoup
import io
from re import findall
from .Database import MyDatabase as db

def extract_R18(page_source):
    base_url_trailer = 'https://awscc3001.r18.com/litevideo/freepv'
    VR_url_trailer = 'https://awscc3001.r18.com/vrsample'
    soup = BeautifulSoup(page_source, 'html.parser').find_all('div', class_ = 'sc-gKAblj boPkKw')
    content = []
    
    for i in range (0, min(len(soup), 5)):
        img_code = soup[i].find('img')
        try:
            code = img_code.attrs['alt']
            if code == '':
                code = 'N/A'

        except:
            code = 'N/A'
            
        img = img_code.attrs['src']
        
        ID = (img.split('/'))[-2]
        fistLetter = ID[0]
        fist3Letter = ID[0:3]
        
        if 'vr' in ID.lower():
            trailer_url = f'{VR_url_trailer}/{fistLetter}/{fist3Letter}/{ID}/{ID}vrlite.mp4'
            
        else:
            trailer_url = f'{base_url_trailer}/{fistLetter}/{fist3Letter}/{ID}/{ID}_dmb_w.mp4'

        detail = soup[i].find('div', class_ = 'sc-pNWxx dryRrI').find_all('div')
        detail = detail[:-1]

        if len(detail) == 2:
            info = {
                'actor' : 'N/A',
                'movie_name' : detail[1].text,
                'code' : code,
                'image' : img,
                'trailer' : trailer_url,
            }

        else:
            info = {
                'actor' : detail[1].text,
                'movie_name' : detail[2].text,
                'code' : code,
                'image' : img,
                'trailer' : trailer_url,
            }
            
        content.append(info)

    return content  

def extract_Xlist(page_source):
    av = db.getCollection("jav")
    soup = BeautifulSoup(page_source, 'html.parser').find_all('li', class_ = 'clearfix')

    getActress = []
    for i in soup:
        info = i.find('h3').text.split(' - ')
        name = info[0].strip()
        try:
            similar = (findall('\d+\.\d+%', info[2]))[0]
        except IndexError:
            similar = (findall('\d\.\d+%', info[1]))[0]
        except:
            similar = (findall('\d\.\d+%', info[2]))[0]     

        moreInfo = av.find_one({'actor' : name})

        avatar = i.find('img').attrs['src']
        cup = measurements = height = 'Unknown'
        if moreInfo:
            avatar = moreInfo['image']
            cup = moreInfo['Cup']
            measurements = moreInfo['Measurements']
            height = moreInfo['Height']

        info = {
            'actor' : name,
            'similar' : similar,
            'cup' : cup,
            'height' : height,
            'measurements' : measurements,
            'avatar' : avatar
        }

        getActress.append(info)

    return getActress

async def AVdebut(month : int, year : int):
    av = db.getCollection('jav')
    return av.find({'Month debut' : month, 'Year debut' : year})

async def AVinfo(actor : str):
    av = db.getCollection('jav')
    return av.find_one({'actor' : actor})

def is_url_image(image_url):
    try:
        if image_url == None:
            return False
        
        image_formats = ("image/png", "image/jpeg", "image/jpg", 'image/webp', 'image/gif')
        r = get(image_url, headers = headerImage, timeout = 10)

        if r.headers["content-type"] in image_formats:
            if int(r.headers['content-length'])/(1024**2) <= 8:
                return True
        return False

    except:
        return False
    
def getURLimage(url = None, ctx = None):
    imgType = ["bmp", "gif", "jpg", "png", "psd", "pspimage", "thm",
                "tif", "yuv", "ai", "drw", "eps", "ps", "svg", "tiff",
                "jpeg", "jif", "jfif", "jp2", "jpx", "j2k", "j2c", "fpx",
                "pcd", "png", "pdf", "webp", "gif"]

    if url != None: 
        if is_url_image(url):
            return url
        
        else:
            return None

    else:
        try:
            data = ctx.message.attachments[0]
            file = data.filename
            url_image = None

            for image_type in imgType:
                if file.endswith(image_type):
                    url_image = data.url
                    break
            
            if url_image is None:
                return None
                
            if is_url_image(url_image):
                return url_image
            return None
        
        except:
            return None
        
def CreateImage(url : str, image_name : str):
    resp = get(url, stream=True, headers = headerImage)
    img = Image.open(io.BytesIO(resp.content))

    try:
        img.save(image_name)
        return True

    except OSError:
        rgb_im = img.convert('RGB')
        rgb_im.save(image_name)
        return True

    except:
        return False