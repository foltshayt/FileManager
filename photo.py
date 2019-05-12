from PIL import Image, ImageEnhance
import media
import copy

class Photo(media.Media):
    def __init__(self, thePathToTheFile):
        super().__init__(thePathToTheFile)
        self.size = self.objectMedia.size
        self.format = self.formatMedia()
        self.objectMediaScaling = copy.deepcopy(self.objectMedia)




    def _openMedia(self, thePathToTheFile):
        """Создает обьект фото"""
        return Image.open(thePathToTheFile)



    def croppingMedia(self, area):
        '''Обрезка видео, фото, музыки'''
        #self.objectMedia.show()

        self.objectMedia = self.objectMedia.crop(area)  #area в формате (left, top, right, bottom)
        self.addHistoryChange()

    def resizePhoto(self, size: tuple):
        """Изменение размера фото"""
        self.objectMedia = self.objectMedia.resize(size)  # size - указываем размер (x, y)
        self.addHistoryChange()

    def transposePhoto(self, direction):    #direction - Как отобразить фото
        """Зеркальное отображение изображения"""
        if direction == "left-right":
            self.objectMedia = self.objectMedia.transpose(Image.FLIP_LEFT_RIGHT)
        elif direction == "top-bottom":
            self.objectMedia = self.objectMedia.transpose(Image.FLIP_TOP_BOTTOM)
        self.addHistoryChange()


    def rotatePhoto(self, direction): #direction - Куда повернуть фото
        """Поворот фото"""
        if direction == "left":
            self.objectMedia = self.objectMedia.transpose(Image.ROTATE_90)
        elif direction == "right":
            self.objectMedia = self.objectMedia.transpose(Image.ROTATE_270)
        self.addHistoryChange()


    def filterConversionPhoto(self, mode):
        """Конвертация фильтров"""
        if mode == "1":   #Черно-белый
            self.objectMedia = self.objectMedia.convert("1")
        elif mode == "L": #Градация серого
            self.objectMedia = self.objectMedia.convert("L")
        elif mode == "CMYK":
            self.objectMedia = self.objectMedia.convert("CMYK")
        self.addHistoryChange()

    def contrastPhoto(self, level):
        self.objectMedia = ImageEnhance.Contrast(self.objectMedia).enhance(level)
        self.addHistoryChange()


    def brightnessPhoto(self, level):
        """Яркость фото регулирование"""
        self.objectMedia = ImageEnhance.Brightness(self.objectMedia).enhance(level)
        self.addHistoryChange()

    def colorBalancPhoto(self, level):
        '''Регулировка цветового баланса'''
        self.objectMedia = ImageEnhance.Color(self.objectMedia).enhance(level)
        self.addHistoryChange()

    def sharpnessPhoto(self, level):
        '''Регулировка резкости изображения'''
        self.objectMedia = ImageEnhance.Sharpness(self.objectMedia).enhance(level)
        self.addHistoryChange()

    def scalingPhoto(self, level):
        if level < 0:
            level = abs(level)
            self.objectMediaScaling = self.objectMediaScaling.resize((self.objectMedia.height * level, self.objectMedia.width * level))
        #aif self.objectMedia.width > 1028 or self.objectMedia.height > 1028:
          #  if self.objectMedia.height > self.objectMedia.width:
               # factor = 1028 / self.objectMedia.height
            #else:
             #   factor = 1028 / self.objectMedia.width
        else:self.objectMediaScaling = self.objectMediaScaling.resize((int(self.objectMedia.height  / level), int(self.objectMedia.width  / level)))

    def writeMedia(self, numberKesh = "", *, path = "kesh\\temp" ):
        '''Запись видео'''
        path += numberKesh + "."
        self.objectMedia.save(path + self.format)








    def infoMedia(self):
        """Информация об обьекте, для статус бара"""
        return self.size, self.format



if "__main__" == __name__:
    a = Photo("Media\\sa.png")
    #a.croppingMedia((15, 100,200,200))
    #a.sharpnessPhoto(4)
    #a.filterConversionPhoto
    #maxsize = (54, 54)
   # a.objectMedia.thumbnail(maxsize, Image.ANTIALIAS)
    #a.objectMedia.show()

    a.scalingPhoto()
    a.objectMediaScaling.show()
    #a.contrastPhoto(2)
    print("aa")
    #a.objectMedia.show()
    #a.writeMedia()
    #a.deleteMedia()
