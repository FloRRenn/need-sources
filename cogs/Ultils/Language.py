def AllowToUseCommand(lang : str = 'vi'):
    if lang == 'vi':
        return f'Admin không cho phép sử dụng lệnh này trong kênh. Các kênh được phép sử dụng lệnh này: '
    
    else:
        return f'You are not allowed to use this command in this channel. Some channels are allowed to use this one: '
    
def InputImageError(lang : str = 'vi'):
    if lang == 'vi':
        return 'Hãy nhập ảnh/video cần tìm\n```s.anime ảnh/video```'
    return 'Please input your image/video\n```s.anime image/video```'

def NotFoundSource(lang : str = 'vi'):
    if lang == 'vi':
        buttonSave = 'Lưu sauce'
        remainder = "**Loại bỏ viền đen và những chi tiết không cần thiết có thể sẽ cho kết quả tốt hơn :)**"
        mess = 'Tui không chắc là có thể tìm đúng nguồn cho bạn'
        source = 'Nguồn'
        recommend = '🔍 Dưới đây là một vài kết quả tui có được từ các công cụ khác'
    
    else:
        buttonSave = 'Save sauce'
        remainder = "**Remove black boders and unnecessary details on your image to get a better result :)**"
        mess = "I'm not sure that i can find this image's source correctly, but...."
        source = 'Source'
        recommend = '🔍 I have some results from orther Seach Engines'
        
    return (remainder, mess, source, recommend, buttonSave)

def FoundSource(lang : str = 'vi'):
    if lang == 'vi':
        similarity = 'Kết quả tương đồng khoảng'
        author = 'Tác giả'
        charactersNames = 'Tên nhân vật'
        source = 'Nguồn'
        media = 'Phim/Game'
        part = 'Tập'
        est_time = 'Thời điểm xuất hiện'
        orther = '**Các kết quả khác**'
        buttonSave = 'Lưu sauce'
        watch = 'Xem phim'
        
    else: 
        similarity = 'Similar to'
        author = 'Author'
        charactersNames = 'Character name'
        source = 'Source'
        media = 'Film/Game'
        part = 'Part'
        est_time = 'Est time'
        orther = '**Orther results**'
        buttonSave = 'Save sauce'
        watch = 'Watch this movie'
        
    return (similarity, author, charactersNames, source, media, part, est_time, orther, buttonSave, watch)

def comeLimitation(lang : str = 'vi', timestamp : str = ''):
    if lang == 'vi':
        return f'**Server của bạn đã hết lượt sử dụng cho ngày hôm nay (50 lượt/ngày). Thời gian reset lượt dự kiến là** ``{timestamp}``'
    return f'**Your server was came to limitation of using this feature (50 times/day). Please try again after** ``{timestamp}``'

def SourceError(code : int, lang : str = 'vi'):
    if lang == 'vi':
        if code == 0:
            return '**Vui lòng nhập ảnh/video cần tìm**\n```s.anime ảnh/video```'
        
        elif code == 1:
            return '**Tui chỉ có thể đọc được các file có định dạng như:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.mp4`, `.mov`\n**Và file phải có dung lượng dưới** `15 mb`'
        
        elif code == 2:
            return '**Vui lòng chọn ảnh/video khác có dung lượng dưới** `15 mb`.'
        
        elif code == 3: 
            return '**Tui không thể truy cập đến ảnh/video này, hãy sử dụng 1 link khác.**'
        
    else:
        if code == 0:
            return '**Input your image or video**\n```s.anime image/video```'
        
        elif code == 1:
            return '**Your file must be an image or a video (** `.png`, `.jpg`, `.jpeg`, `.gif`, `.mp4`, `.mov` **) and size is under** `15 mb`.'
        
        elif code == 2:
            return '**This file/link acrosses the limit of size (** `15 mb` **). Please input another file/link**'
        
        elif code == 3:
            return '**I can not access to this link. Please input another link**'

def ReverseSearch(lang : str = 'vi'):
    if lang == 'vi':
        SeeMore = 'Xem thêm'
        similarImage = 'Ảnh tương tự'
        result = 'Kết quả tìm được từ'
        error1 = 'Không tìm thấy kết quả. Có thể bot đã bị chặn bởi **Capcha**. Vui lòng tìm kiếm thủ công bằng cách click vào nút `Xem thêm` bên dưới.'
        error2 = 'Tui chỉ có thể đọc file ảnh có đuôi là `.png`, `.jpg` `.jpeg` `.gif`'
        
    else:
        SeeMore = 'Find more'
        similarImage = 'Similar images'
        result = 'Results from'
        error1 = 'Not found any result. Maybe bot is prevented accessing from browser. Please try again later or find that image by clicking to buttons below.'
        error2 = 'I just find image wiht exten is `.png`, `.jpg`, `.jpeg`, `.gif`'
        
    return (SeeMore, similarImage, result, error1, error2)

def SetupCMD(cmd : str, lang : str = 'vi'):
    if lang == 'vi':
        dontAdd = f'**Bạn đã thêm lệnh `{cmd}` vào trước đó rồi!!**'
        Notsuccessful = f'**Không tìm thấy lệnh `{cmd}` trong danh sách. Vui lòng xem lại!!**'
        
    else:
        dontAdd = f'**You have add command `{cmd}` for this channel before!!**'
        Notsuccessful = f'**Can not found thid `{cmd}`, please try again!!!**'
    return (dontAdd, Notsuccessful)

def setupSucessful(listCMD : list, lang : str = 'vi'):
    if lang == 'vi':
        return f'**Đã setup thành công cho các lệnh {listCMD} cho kênh**'
    return f'**Added successfully for {listCMD} in**'

def delCMDMess(lang : str = 'vi'):
    if lang == 'vi':
        lostARG = '**Hãy cho tui biết đúng lệnh bạn cần xóa. Nếu bạn không biết, hãy thử `s.manage` để xem các ràng buộc.**'
        successful = '**Đã xóa thành công!!**'
        unsuccessful = '**Bạn không áp đặt lệnh đó cho kênh này.**'
        
    else:
        lostARG = '**Please, give me a name of command you want to delete like `anime`, `face`, .... If you do not know what command is allowed in this channel, please try `s.manage` for more detail.**'
        successful = '**Delete successful**'
        unsuccessful = '**You do not have any constraint for this channel.**'
        
    return (lostARG, successful, unsuccessful)
        
def rule34Mess(lang : str = 'vi'):
    if lang == 'vi':
        return '**Không tìm thấy bất kỳ ảnh liên quan**'
    return '**Can not find any images with this tag**'

def SaveImage(lang : str = 'vi'):
    if lang == 'vi':
        return 'Lưu ảnh trên'
    return 'Save this image'

def SaveVideo(lang : str = 'vi'):
    if lang == 'vi':
        return 'Lưu video trên'
    return 'Save this video'

def WaifuError(cmd : str, tag : str, lang : str = 'vi'):
    if lang == 'vi':
        return f'Không tìm thấy `{tag}`, hãy thử [ `{cmd} tag` ] để xem các tag có thể sử dụng.'
    return f'I do not have tag `{tag}`, try [ `{cmd} tag` ] to get available tags.'

def HentaiTagError(tag : str, lang : str = 'vi'):
    if lang == 'vi':
       return f'Không tìm thấy tag `{tag}`. Hãy thử một tag khác!!'
    return f'Can not find any commic with tag `{tag}`. Please select another tag.'

def HentaiMess(id : int, lang : str = 'vi'):
    if lang == 'vi':
        notFoundID = f'**Không tìm thấy truyện có ID:** `{id}`'
        isLoli = '**Không thể xem truyện này vì có chứa nội dung không phù hợp với Guidelines của Discord.**'
        commic = 'Tên truyện'
        author = 'Tác giả'
        totalPages = 'Tổng số trang'
        watch = 'Click 🔽 để xem truyện.\nClick 💾 để lưu trang truyện hiện tại.'
        move = f'Click ⬅️ | ➡️ để xem truyện tiếp theo - Gõ [ s.id {id} ] để xem truyện này.'
        
    else:
        notFoundID = f'**Can not find commic with ID: `{id}`**'
        isLoli = "**Can not show content of this commic because of Discord's Guidelines**"
        commic = 'Name of commic'
        author = 'Author'
        totalPages = 'Total pages'
        watch = 'Click 🔽 to read this commic.\nClick 💾 to save cunrrent page.'
        move = f'Click ⬅️ | ➡️ to move to new commic - Type [ s.id {id} ] to read this commic'
    return (notFoundID, isLoli, commic, author, totalPages, watch, move)

def ShowHentaiPage(lang : str = 'vi'):
    if lang == 'vi':
        page = 'Trang'
        commic = 'truyện'
        save = 'Click vào 💾 để lưu trang truyện này.'
        move = 'Click vào 🔽 để xem các trang tiếp theo.'
        
    else:
        page = 'Page'
        commic = 'commic'
        save = 'Click 💾 to save this page.'
        move = 'Click 🔽 to move to new page.'
    return (page, commic, save, move)
        
def DebutMess(ctx, lang : str = 'vi'):
    if lang == 'vi':
        mess1 = '**Chỉ nhập tháng và năm. Ví dụ** `s.debut 11/2021`'
        mess2 = '**Chỉ được nhập số. Ví dụ** `s.debut 11/2021`'
        mess3 = '**Một năm chỉ có 12 tháng**'
        mess4 = '**Xin lỗi, tui có dữ liệu từ năm 2020 đến bây giờ.**'
        mess5 = '**Chỉ được nhập tháng nhỏ hơn hoặc bằng tháng hiện tại. Ví dụ:**'
        mess6 = f'**Thông tin được gửi riêng cho {ctx.author.mention} để tránh spam quá nhiều trong kênh chat**'
    
        mess8 = 'Ngày sinh'
        mess9 = 'Cung'
        mess10 = 'Quê quán'
        mess11 = 'Cup size'
        mess12 = 'Chiều cao'
        mess13 = 'Số đo 3 vòng'
        mess14 = 'Thể loại'
        mess15 = 'Ngày debut'
        mess16a = '**Xin lỗi, hiện tại tui không có dữ liệu của tháng**'
        mess16b = '**(Có thể là chưa có ai debut trong khoảng thời gian này)**'
        mess17a = '**Tổng cộng có**'
        mess17b = '**diễn viên debut trong tháng**'
    
    else:
        mess1 = '**Just input day and year**\n```s.debut 11/2021```'
        mess2 = '**Just input the number of day and year**\n```s.debut 11/2021```'
        mess3 = '**It just have 12 months of a year**'
        mess4 = '**I just have data from 1/2020 to now**'
        mess5 = '**Just input a number of month that is equal or smaller than current month**'
        mess6 = f'**The information is sent to {ctx.author.mention} because of avoiding to spam too much in channel.**'
        
        mess8 = 'Date of Birth'
        mess9 = 'Zodiac'
        mess10 = 'Place of Birth'
        mess11 = 'Cup size'
        mess12 = 'Height'
        mess13 = 'Measurements'
        mess14 = 'Catagories'
        mess15 = 'Date of Debut'
        mess16a = '**Sorry, I do not have any information on**'
        mess16b = '**Maybe, there is no one debut in this month now.**'
        mess17a = '**There are**'
        mess17b = '**actress(es) are debut on**'
        
    return (mess1, mess2, mess3, mess4, mess5, mess6, mess8, mess9, mess10, mess11,mess12,mess13,mess14,mess15,mess16a,mess16b,mess17a,mess17b)

def JAVmess(lang : str = 'vi'):
    if lang == 'vi':
        error1 = '**Không tìm thấy code phim từ bức ảnh này. Vui lòng sử dụng 1 bức ảnh khác có nội dung rõ ràng hơn.**'
        save = 'Lưu phim'
        film = 'Phim đề xuất'
        exten_error = '**Xin lỗi, tui chỉ có thể xem được file ảnh như** `.jpg`, `.png`, `.jpeg`'
        
    else:
        error1 = '**I can not find any movie with this image. Please use another image have content clearly.**'
        save = 'Save this movie' 
        film = 'Movie'
        exten_error = '**Sorry, I just work with file ** `.jpg`, `.png`, `.jpeg`'
    return (error1, save, film, exten_error)

def FACEmess(lang : str = 'vi'):
    if lang == 'vi':
        error1 = '**Không thể nhận ra diễn viên từ bức ảnh này. Vui lòng sử dụng 1 bức ảnh khác có khuôn mặt rõ ràng hơn rõ ràng hơn.**'
        save = 'Lưu info'
        similarity = 'Tương đồng khoảng'
        height = 'Chiều cao'
        measurements = 'Số đo theo tiêu chuẩn Nhật Bản (cm)'
        exten_error = '**Xin lỗi, tui chỉ có thể xem được file ảnh như** `.jpg`, `.png`, `.jpeg`'
        
    else:
        error1 = '**I can not recognite any actress from this image. Please, use another image that have a face clearly.**'
        save = 'Save this info'
        similarity = 'Similar to'
        height = 'Height'
        measurements = 'Measurements (cm)'
        exten_error = '**Sorry, I just work with file ** `.jpg`, `.png`, `.jpeg`'
        
    return (error1, save, similarity, height, measurements, exten_error)

def RandomMovieMess(tag : str, lang : str = 'vi'):
    if lang == 'vi':
        save = 'Lưu phim'
        duration = "Thời lượng"
        error = f'**Không tìm thấy tag** `{tag}`**. Hãy thử [ `s.code tag` ] để xem các tag khả dụng.**'
        
    else:
        save = 'Save this movie' 
        duration = 'Duration'
        error = f'**I can not find any movie with tag** `{tag}`**. Please try [ `s.code tag` ] to get available tags.**'
        
    return (save, duration, error)

def CommandNotFoundMess(lang : str = 'vi'):
    if lang == 'vi':
        return '**Tui không có lệnh này. Có thể bạn đã nhập sai, hãy gõ [ `s.help` ] để được trợ giúp.**'
    return '**I do not have this command. Please try [ `s.help` ] for help**'

def BadArgumentMess(lang : str = 'vi'):
    if lang == 'vi':
        return '**Bạn đã ghi sai cú pháp của lệnh trên. Hãy thử [ `s.help tên_lệnh` ] để xem cú pháp đúng.**'
    return '**Bad argument. Please try [ `s.help command_name` ] for help.**'

def MissingRequiredArgumentMess(lang : str = 'vi'):
    if lang == 'vi':
        return '**Bạn chưa đủ ghi dủ yêu cầu của lệnh này. Hãy thử [ `s.help tên_lệnh` ] để xem cú pháp đầy đủ.**'
    return '**You have missed the required argument. Please try [ `s.help command_name` ] for help.**'

def TimeFormat(time, lang : str = 'vi'):
    format = {
        'vi' : ['phút', 'giây'], 
        'en' : ['min', 'sec']
    }
    
    if time < 60:
        return f'{round(time, 2)} {format[lang][1]}'
    
    time = round(time) 
    minutes = time // 60
    seconds = time % 60 
    return f'{minutes} {format[lang][0]} {seconds} {format[lang][1]}'
            

def CommandOnCooldownMEss(time, lang : str = 'vi'):
    if lang == 'vi':
        return 'Quá nhiều yêu cầu được gửi trong khoảng thời gian quá ngắn. Vui lòng thử lại sau **{}**.'.format(TimeFormat(time, lang))
    return 'Too much requests in short time. Please try again after **{}**.'.format(TimeFormat(time, lang))

def NSFWChannelRequiredMess(lang : str = 'vi'):
    if lang == 'vi':
        return '**Chỉ được dùng lệnh này trong kênh NFSW (Kênh 18+).**'
    return '**This command can be used in NSFW channels (18+).**'

def MissingPermissionsMess(lang : str = 'vi'):
    if lang == 'vi':
        return '**Chỉ người có quyền quản trị (admin) mới được phép dùng lệnh này.**'
    return '**Just admin or person have role manage can use this command.**'

def NoPrivateMessageMess(lang : str = 'vi'):
    if lang == 'vi':
        return "**Tui không thể trả lời tin nhắn riêng của bạn. Hãy quay lại server để có thể dùng tiếp.**"
    return "**You can not use this command in private. Please, back to the server to use this one.**"

def UnknownErrorMess(lang : str = 'vi'):
    if lang == 'vi':
        return '**Lỗi! Vui lòng thử lại sau.\n Nếu lỗi xuất hiện liên tục, bạn hãy dùng ** `s.report` **để thông báo lỗi. Không được dùng lệnh này để spam, nếu không bạn sẽ cấm dùng tất cả lệnh của tui!!**\n```s.report tên_lệnh_và_mô_tả_lỗi```'
    return '**Error!! Please try later. \nIf this error appears regularly, please report to me by using ** `s.report`. **Do not use this command for spamming, unless you will be mute from using my commands**\n```s.report command_name_and_your_description```'

def TryAgain(lang : str = 'vi'):
    if lang == 'vi':
        return '**Vui lòng thử lại!**'
    return '**Please, try again!**'

def Feedback(lang : str = 'vi'):
    if lang == 'vi':
        return '**Đã gửi feedback thành công!!**'
    return '**Your feedback is sent successfully!!**'

def FeedbackError(lang : str = 'vi'):
    if lang == 'vi':
        return '**Hãy nhập cảm nghĩ của bạn!!**'
    return '**Let me know your feedback!!**'

def lengthError(lang : str = 'vi'):
    if lang == 'vi':
        return '**Nội dung feedback phải ít hơn 2000 ký tự**'
    return '**Your feedback must be less than 2000 characters in length**'

def BooruError(cmd : str ,lang : str = 'vi'):
    if lang == 'vi':
        return f'```Không tìm bất kỳ ảnh hay video nào. Hãy nhập tag giống ví dụ dưới đây:\n--> s.{cmd} genshin_impact \nHoặc\n--> s.{cmd} genshin_impact video```'
    return f'```I can not find any image or video about this tag. Please input your tag like this example:\n--> s.{cmd} genshin_impact \nOR\n--> s.{cmd} genshin_impact video```'

def SauceNao_checkAPI(lang : str = 'vi'):
    if lang == 'vi':
        successful = '**Đã thêm api này vào server của bạn**'
        error = '**Đây không phải là api hợp lệ, vui lòng nhập 1 api khác**'
        
    else:
        successful = '**Added your api successfully**'
        error = '**This is an invalid API key**'
    return (successful, error)