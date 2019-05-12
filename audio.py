from moviepy import editor
from moviepy import audio
from  pydub import AudioSegment
import media

class Audio(media.Media):
    def __init__(self, thePathToTheFile):
        super().__init__(thePathToTheFile)
        #self.size = self.objectMedia.size
        self.format = self.formatMedia()
        self.audio = [True, True] #1 -True, значит аудио есть в видео, 2 - если будет ложь то Отключает при первом ложе возможность повторного запуска функции


    def _openMedia(self, thePathToTheFile):
        """Создает медиа обьект"""
        return audio.io.AudioFileClip.AudioFileClip(thePathToTheFile)
        #return  AudioSegment.from_mp3(thePathToTheFile )

    def croppingMedia(self, section_start, section_finish):  # section - отрезок в секундах
        '''Обрезка видео, фото, музыки'''
        self.objectMedia = self.objectMedia.subclip(section_start, section_finish)
        #print(section_start * 1000, section_finish * 1000)
        #self.objectMedia = self.objectMedia[section_start * 1000:section_finish * 1000]
        self.addHistoryChange()


    def removeAudio(self, section_start, section_finish):
        '''Пропускает данный фрагмент'''
        self.objectMedia = self.objectMedia.cutout(section_start, section_finish)
        self.addHistoryChange()





    def writeMedia(self, numberKesh ="", *, path = r"kesh\temp"):
        '''Запись видео'''
        path += numberKesh + "."
        print("Start")
        try:

            self.objectMedia.write_audiofile(path + self.format, buffersize=200)
        except:
            print("Error записи")
        print("write")

        print("Start")
        '''
        try:    
            self.objectMedia.export(path + self.format, format=self.format)
        except Exception as a:
            print(a,"eror")
        else:
            print("finish")
        '''
    def infoMedia(self):
        """Информация об обьекте, для статус бара"""
        pass

if "__main__" == __name__:
    a = Audio("Media\\imagine-dragons-natural.mp3")
    #a.screenshotVideo("Ola",(0,5))
    #a.remove_audioVideo()
    #a.objectMedia.preview()
    #a.titleVideo("assassaassaa")
    #a.croppingMedia("0:0:05", "0:0:25")
    a.removeAudio("0:0:05", "0:0:25")
    a.objectMedia.preview()
    a.writeMedia()
    print(":as")
