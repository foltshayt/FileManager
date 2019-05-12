from abc import ABCMeta, abstractmethod


class Media(metaclass= ABCMeta):
    quantityHistory = 20  #Размер истории событий медиа файла

    def __init__(self, thePathToTheFile):
        self.pathMedia = thePathToTheFile
        self.objectMedia = self._openMedia(thePathToTheFile)
        self.history = [self.objectMedia]

        self._currentHistoryNumber = 0
        pass

    @abstractmethod
    def _openMedia(self, thePathToTheFile):
        """Создает медиа обьект"""
        pass

    @abstractmethod
    def croppingMedia(self):
        '''Обрезка видео, фото, музыки'''
        pass

    @abstractmethod
    def writeMedia(self, *, path):
        '''Запись видео'''
        pass


    def deleteMedia(self):
        import os
        #self.objectMedia.show()
        #self.objectMedia = None
        os.remove(self.pathMedia)

    @abstractmethod
    def infoMedia(self):
        """Информация об обьекте, для статус бара"""
        pass

    def addHistoryChange(self):
        '''Добавляет при каждом дейтсвии в историю обьект'''
        self.history = self.history[: self._currentHistoryNumber + 1] #Очищает историю если мы вернулись назад по истории и начали редактировать от этого места
        self.history.append(self.objectMedia)
        self._currentHistoryNumber += 1
        if Media.quantityHistory < len(self.history): # Если размер допустимой истории меньше чем размер списка исории то очищаем его
            del self.history[1]

    def backHistoryChange(self):
        '''Возвращаемся к предыдущей истории'''
        if self._currentHistoryNumber != 0:
            self._currentHistoryNumber -= 1
            self.objectMedia = self.history[self._currentHistoryNumber]
            self.writeMedia()

    def nextHistoryChange(self):
        '''К следующей истории'''
        if self._currentHistoryNumber < len(self.history) - 1:
            self._currentHistoryNumber += 1
            self.objectMedia = self.history[self._currentHistoryNumber]
            self.writeMedia()


    def formatMedia(self):
        '''Возвращает формат медиа файла'''
        return self.pathMedia[self.pathMedia.rfind(".") + 1:]


