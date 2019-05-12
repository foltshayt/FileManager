def сonversionToSeconds(time):
    '''Конвертация времени формата "h:m:s" в секунды'''
    time = list(map(lambda time: int(time), time.split(":")))
    second = time[0] * 3600 + time[1] * 60 + time[2]
    return second

def playlistSort(types, playlist):
    if types == "photo":
        playlist = filter(lambda media: media[media.rfind(".") + 1:] in  {"png", "jpg", "JPG"}, playlist)
        print(playlist)


