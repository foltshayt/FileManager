from moviepy import editor

import media


class Video(media.Media):
    def __init__(self, thePathToTheFile):
        super().__init__(thePathToTheFile)
        #self.size = self.objectMedia.size
        self.format = self.formatMedia()
        self.audio = [True, True] #1 -True, значит аудио есть в видео, 2 - если будет ложь то Отключает при первом ложе возможность повторного запуска функции


    def _openMedia(self, thePathToTheFile):
        """Создает медиа обьект"""
        return editor.VideoFileClip(thePathToTheFile)


    def croppingMedia(self, section_start, section_finish): #section - отрезок в секундах
        '''Обрезка видео, фото, музыки'''
        self.objectMedia = self.objectMedia.subclip(section_start, section_finish)
        self.addHistoryChange()


    def titleVideo(self, textV, colorV= "red", sizeV=(1920,1080), bg_colorV= "white", fontsizeV = 30, set_duration = 3):
        title = editor.TextClip(txt=textV, color= colorV, size = sizeV, bg_color = bg_colorV, fontsize=fontsizeV)
        title.set_duration(set_duration) #Устанавливает продолжительность
        self.objectMedia = editor.concatenate_videoclips([title,self.objectMedia])
        self.addHistoryChange()


    def screenshotVideo(self, nameFile, time):
        print(nameFile)
        self.objectMedia.save_frame(nameFile, t = time)
        self.writeVideo()
        self.addHistoryChange()

    '''
    def transparencyVideo(self, value):
        #Уровень непрозрачности клипа
        self.objectMedia = self.objectMedia.set_opacity(value)
    '''

    def remove_audioVideo(self):
        '''Удалить аудио из клипа'''
        self.objectMedia = self.objectMedia.without_audio()
        #self.writeVideo()
        self.addHistoryChange()


    def writeMedia(self, numberKesh = "", *, path = "kesh\\temp"):
        '''Запись видео'''
        path += numberKesh + "."
        self.objectMedia.write_videofile(path + self.format)

    def resizeClip(self, width):
        self.objectMedia = self.objectMedia.resize(width=500, height= 800)
        self.addHistoryChange()

    def concatenateVideo(self, clip1,clip2, i = 0):
        clip1 = clip1.objectMedia.set_fps(25)
        clip2 = clip2.objectMedia.set_fps (25)
        if i:

            clip2, clip1 = clip1, clip2
        self.objectMedia = editor.concatenate_videoclips([clip1, clip2 ])
        self.addHistoryChange()




    def infoMedia(self):
        """Информация об обьекте, для статус бара"""
        pass
if "__main__" == __name__:
    a = Video("Video\\fas.mp4")
    a.resizeClip("360")
    #a.screenshotVideo("Ola",(0,5))
    #a.remove_audioVideo()
    #a.objectMedia.preview()
    #a.titleVideo("assassaassaa")
    #
    b = Video("Media\\as.mp4")
    b.resizeClip("360")
    a.concatenateVideo(a,b)

    #a.objectMedia.preview()
    a.writeMedia(str(1))
