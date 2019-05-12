import sys
from PyQt5 import  QtWidgets, uic, QtCore
from PyQt5 import QtMultimedia, QtMultimediaWidgets


import os
from PyQt5 import QtGui
from PyQt5.QtGui import QImage
from PIL import Image
from PIL.ImageQt import ImageQt
import photo, video, audio

from additionalModules import  additionalModules



class MediaQt(QtWidgets.QMainWindow):
    open = True
    def __init__(self, parent=None):
        self.activeButton = []
        super().__init__()
        self.path=""
        self.mediaQt = uic.loadUi("mediaQt.ui")
        self.menuBar()
        self.toolBar()
        self.mediaQt.editPanelPhotoButtonBox.accepted.connect(self.slotSignalPhotoEditPanel)
        self.mediaQt.editPanelVideoButtonBox.accepted.connect(self.slotSignalVideoEditPanel)
        self.mediaQt.editPanelAudioButtonBox.accepted.connect(self.slotSignalAudioEditPanel)
        self.slotSignalVideoButtonEditPanel()
        self.slotSignalPhotoButtonEditPanel()
        self.playlistButton()
        self.mediaQt.show()


        self.numberKesh = 0 #Номер файла в кеше

        self.listPlaylist = [] #Список ссылок на медиа обьекты
        self.indexLinkPlaylist =  0 #Номер текущей ссылки на обьект в прейлисте




    def startMedia(self):
        if self.fileType in {"mp4"}:
            if not hasattr(self, "player"): #Если медиаплеер существует то больше его не создавать
                self.player = QtMultimedia.QMediaPlayer()

            if  not hasattr(self, "viewer"): #Если проигрыватель существует не создавать больше его
                self.viewer = QtMultimediaWidgets.QVideoWidget()
                self.viewer.resize(700, 600)
                self.viewer.move(0, 0)

                self.player.setVideoOutput(self.viewer)
            self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.path)))
            self.hbox = QtWidgets.QHBoxLayout(self.mediaQt.videoMediaWidget)

            self.hbox.addWidget(self.viewer)
            self.player.setPosition(0)


            self.viewer.show()
        elif self.fileType in {"png", "jpg", "JPG"}:
            pix = QtGui.QPixmap()
            pix.load(self.path)

            if MediaQt.open:
                self.hbox = QtWidgets.QHBoxLayout(self.mediaQt.photoMediaWidget)
                self.lbl = QtWidgets.QLabel(self.mediaQt.photoMediaWidget)
                self.lbl.setAlignment(QtCore.Qt.AlignCenter)
                self.hbox.addWidget(self.lbl)
                self.mediaQt.photoMediaWidget.setLayout(self.hbox)
                MediaQt.open = False
            self.lbl.setPixmap(pix)
            self.lbl.repaint()



        elif self.fileType in {"mp3"} :
            if not hasattr(self, "player"):
                self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(self.path)))
            self.hbox = QtWidgets.QHBoxLayout(self.mediaQt.audioMediaWidget)
            self.lbl = QtWidgets.QLabel()
            self.lbl.setAlignment(QtCore.Qt.AlignCenter)
            pix = QtGui.QPixmap()
            pix.load("Icon//mediaWidget//music.png")
            self.lbl.setPixmap(pix)
            self.hbox.addWidget(self.lbl)


        self.slotSignalMusicVideoControlPanel()
        #self.slotSignalPhotoControlPanel()



    def openMedia(self):
        #if hasattr(self, "player"):#Удаляет медиаплеер
            #self.player.deleteLater()
            #del self.player


        if hasattr(self, "hbox"): #Удаляет отрисовку
            self.hbox.deleteLater()
            del self.hbox

        self.pathSourceObject = self.path[:self.path.rfind(".")]
        self.fileType = self.path[self.path.rfind(".") + 1:]
        if self.fileType in {"png", "jpg", "JPG"}:
            self.mediaObject = photo.Photo(self.path)
            self.mediaQt.MediaStackedWidget.setCurrentIndex(1)
            self.mediaQt.editPanelStacked.setCurrentIndex(3)
            self.mediaQt.controlPanelStacked.setCurrentIndex(2)
            self.startMedia()
        if self.fileType in {"mp4"}:
            self.mediaObject = video.Video(self.path)
            self.mediaQt.MediaStackedWidget.setCurrentIndex(0)
            self.mediaQt.editPanelStacked.setCurrentIndex(0)
            self.mediaQt.controlPanelStacked.setCurrentIndex(0)

            self.startMedia()
        elif self.fileType in {"mp3"}:
            self.mediaObject = audio.Audio(self.path)
            self.mediaQt.MediaStackedWidget.setCurrentIndex(2)
            self.mediaQt.editPanelStacked.setCurrentIndex(1)
            self.mediaQt.controlPanelStacked.setCurrentIndex(0)
            self.startMedia()








    def slotSignalPhotoEditPanel(self):
        print(self.mediaQt.resizePhotoWidthSpinBox.value())
        print("Aaaaaqqqq")
        self.сhangeСheck = False


        '''Яркость'''
        if self.mediaQt.resizePhotoWidthSpinBox.value() != 1 and self.mediaQt.resizePhotoHeightSpinBox.value()!=1:
            self.mediaObject.resizePhoto( (self.mediaQt.resizePhotoWidthSpinBox.value(), self.mediaQt.resizePhotoHeightSpinBox.value()))
            self.сhangeСheck = True
        if self.mediaQt.brightSlider.value() != 10:
            self.mediaObject.brightnessPhoto(self.mediaQt.brightSlider.value() /10)
            self.сhangeСheck = True

        '''Контрастность'''
        if self.mediaQt.contrastSlider.value() != 10:
            self.mediaObject.contrastPhoto(self.mediaQt.contrastSlider.value() /10)
            self.сhangeСheck = True

        if not self.mediaQt.filterDefaultRadioButton.isChecked() :
            if self.mediaQt.filterCmykRadioButton.isChecked():self.mediaObject.filterConversionPhoto("CMYK")
            elif self.mediaQt.filterBlacWhiteRadioButton.isChecked(): self.mediaObject.filterConversionPhoto("1")
            elif self.mediaQt.filterGrayscaleRadioButton.isChecked(): self.mediaObject.filterConversionPhoto("L")
            self.сhangeСheck = True


        if "mirrorHorizontal" in self.activeButton:
            self.mediaObject.transposePhoto("left-right")
            self.activeButton.remove("mirrorHorizontal")
            self.сhangeСheck = True

        if "mirrorVertical" in self.activeButton:
            self.mediaObject.transposePhoto("top-bottom")
            self.activeButton.remove("mirrorVertical")
            self.сhangeСheck = True

        if "turnLeft" in self.activeButton:
            self.mediaObject.rotatePhoto("left")
            self.activeButton.remove("turnLeft")
            self.сhangeСheck = True

        if "turnRight" in self.activeButton:
            self.mediaObject.rotatePhoto("right")
            self.activeButton.remove("turnRight")
            self.сhangeСheck = True


        if self.сhangeСheck:   #Запуск записи при условий изменений
            #self.path = "kesh\\temp." + self.mediaObject.format
            #self.mediaObject.writeMedia()
            self.path = "kesh\\temp" + str(self.numberKesh) + "." + self.mediaObject.format
            self.mediaObject.writeMedia(str(self.numberKesh))
            self.numberKesh += 1
        #self.startMedia()
        self.openMedia()

    def slotSignalAudioEditPanel(self):
        self.сhangeСheck = False
        def audioTrimming():
            """Обрезать аудио"""
            startTime =  additionalModules.сonversionToSeconds(self.mediaQt.audioTrimmingStartTimeEdit.time().toString())
            endTime =  additionalModules.сonversionToSeconds(self.mediaQt.audioTrimmingEndTimeEdit.time().toString())
            #startTime = self.mediaQt.audioTrimmingEndTimeEdit.time().toString()
           # endTime = self.mediaQt.audioTrimmingEndTimeEdit.time().toString()

            if startTime != 0 and endTime != 0 and endTime > startTime:
                self.mediaObject.croppingMedia(startTime, endTime)
                self.сhangeСheck = True
            from PyQt5.QtCore import QTime
            standardValue = QTime(00, 00, 00)  # Время начала
            self.mediaQt.audioTrimmingStartTimeEdit.setTime(standardValue)  # Устанавливаем стандартное время
            self.mediaQt.audioTrimmingEndTimeEdit.setTime(standardValue)

        def audioRemove():
            """Удалить часть видео"""
            #startTime =  additionalModules.сonversionToSeconds(self.mediaQt.audioRemoveStartTimeEdit.time().toString())
            #endTime =  additionalModules.сonversionToSeconds(self.mediaQt.audioRemoveEndTimeEdit.time().toString())
            startTime = self.mediaQt.audioRemoveStartTimeEdit.time().toString()
            endTime = self.mediaQt.audioRemoveEndTimeEdit.time().toString()
            if startTime != "00:00:00" and endTime != "00:00:00" :
                self.mediaObject.removeAudio(startTime, endTime)
                self.сhangeСheck = True
            from PyQt5.QtCore import QTime
            standardValue = QTime(00, 00, 00)  # Время начала
            self.mediaQt.audioRemoveStartTimeEdit.setTime(standardValue)  # Устанавливаем стандартное время
            self.mediaQt.audioRemoveEndTimeEdit.setTime(standardValue)


        def speedPlay():
            """Изменить скорость воспроизведения"""
            speed = self.mediaQt.speedPlayAudioHorizontalSlider.value()
            if speed < 0:
                speed = abs(speed) / 10
                self.player.setPlaybackRate(speed)
            else:
                speed += 1
                self.player.setPlaybackRate(speed)


        speedPlay()
        audioRemove()
        audioTrimming()  # Обрезание аудио
        if self.сhangeСheck:   #Запуск записи при условий изменений

            self.path = "kesh\\temp" + str(self.numberKesh) + "." + self.mediaObject.format
            self.mediaObject.writeMedia(str(self.numberKesh))
            self.numberKesh += 1
        #self.startMedia()
        self.openMedia()

    def slotSignalVideoEditPanel(self):
        """Проверка на нажати выключения аудио, и остановить повторное срабатывание"""
        self.сhangeСheck = False  # Проверка были ли изменения если да то запускает запись

        if not self.mediaObject.audio[0] and self.mediaObject.audio[1] :
            self.mediaObject.remove_audioVideo()
            self.mediaObject.audio[1] = False
            self.сhangeСheck = True


        def videoTrimming():
            """Обрезание видио"""

            startTime = additionalModules.сonversionToSeconds(self.mediaQt.videoTrimmingStartTimeEdit.time().toString())
            endTime = additionalModules.сonversionToSeconds(self.mediaQt.videoTrimmingEndTimeEdit.time().toString())
            if startTime != 0 and endTime != 0 and endTime > startTime:
                self.mediaObject.croppingMedia(startTime, endTime)
                self.сhangeСheck = True

            from PyQt5.QtCore import QTime
            standardValue = QTime(00, 00, 00)  #Время начала
            self.mediaQt.videoTrimmingStartTimeEdit.setTime(standardValue) #Устанавливаем стандартное время
            self.mediaQt.videoTrimmingEndTimeEdit.setTime(standardValue )

        def speedPlay():
            """Изменить скорость воспроизведения"""
            speed = self.mediaQt.speedPlayVideoHorizontalSlider.value()
            if speed < 0:
                speed = abs(speed) / 10
                self.player.setPlaybackRate(speed)
            else:
                speed += 1
                self.player.setPlaybackRate(speed)



        speedPlay()
        videoTrimming() #Обрезание видио


        if self.сhangeСheck:   #Запуск записи при условий изменений
            #self.path = "kesh\\temp." + self.mediaObject.format
            self.path = "kesh\\temp" + str(self.numberKesh) + "." + self.mediaObject.format
            #self.mediaObject.writeMedia()
            self.mediaObject.writeMedia(str(self.numberKesh))
            self.numberKesh += 1

        #self.startMedia()
        self.openMedia()


    def slotSignalVideoButtonEditPanel(self):
        def remove_audio():
            self.mediaObject.audio[0] = False

        self.mediaQt.remove_audioButton.clicked.connect(remove_audio)

    def slotSignalPhotoButtonEditPanel(self):
        self.mediaQt.mirrorHorizontalButton.clicked.connect(lambda *args: self.activeButton.append("mirrorHorizontal"))
        self.mediaQt.mirrorVerticalButton.clicked.connect(lambda *args: self.activeButton.append("mirrorVertical"))
        self.mediaQt.turnLeftButton.clicked.connect(lambda *args: self.activeButton.append("turnLeft"))
        self.mediaQt.turnRightButton.clicked.connect(lambda *args: self.activeButton.append("turnRight"))

    #def slotSignalPhotoControlPanel(self):





    def slotSignalMusicVideoControlPanel(self):
        def setSliderPosition():
            '''Устанавливает позицию слайдера'''
            time = self.mediaQt.timeSlider.value() * 1000
            self.player.setPosition(time)

        def mediaDuration(time):
            '''Устанавливает длину слайдера'''
            self.duration = time // 1000
            self.mediaQt.timeSlider.setMaximum(self.duration)


        #Включить проигрование видео
        self.mediaQt.playButton.clicked.connect(lambda *args:self.player.play())

        #Остановить проигрование музыки
        self.mediaQt.stopButton.clicked.connect(lambda *args: self.player.stop())

        #Пауза воспроизвидения видио
        self.mediaQt.pauseButton.clicked.connect(lambda *args: self.player.pause())

        #Громкость звука
        self.mediaQt.volumeSlider.valueChanged.connect(lambda value: self.player.setVolume(value))



        #Текущая позиция слайдера
        try:
            self.player.positionChanged.connect(lambda time: self.mediaQt.timeSlider.setValue(time // 1000))
        except:
             self.mediaQt.timeSlider.setValue(0)
        #Установка позиции спомощью слайдера
        self.mediaQt.timeSlider.sliderMoved.connect(setSliderPosition)

        #Длина слайдера прокрутки видео
        try:
            self.player.durationChanged.connect(mediaDuration)
        except: pass

    def playlistButton(self):
        print("asasasassaas")
        # Предыдущий файл прейлиста
        self.mediaQt.backObjectVideoMusicPushButton.clicked.connect(lambda: self.playlist("back"))
        # Следующий файл прейлиста
        self.mediaQt.nextObjectVideoMusicPushButton.clicked.connect(lambda: self.playlist("next"))

        # Предыдущий файл прейлиста
        self.mediaQt.backObjectPhotoPushButton.clicked.connect(lambda: self.playlist("back"))
        # Следующий файл прейлиста
        self.mediaQt.nextObjectPhotoPushButton.clicked.connect(lambda: self.playlist("next"))

    def menuBar(self):
        def setPath():
            """Окно для выбора файла"""
            path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
            types = path[path.rfind(".") + 1:]

            errorType = False #Есть ли ошибка
            if types not in {"png", "jpg", "JPG", "mp3", "mp4", ""}:
                self.error = uic.loadUi("errorQt.ui")
                self.error.show()
                errorType = True
            if path and not errorType:
                self.path = path
                self.openMedia()

        def setPlaylist():
            self.listPlaylist = QtWidgets.QFileDialog.getOpenFileNames(self, filter=("*.jpg *.png *.mp3 *.mp4"))[0]
            self.indexLinkPlaylist = 0
            if self.listPlaylist:
                self.path = self.listPlaylist[0]
                self.openMedia()

        def setSavePath():
            path = QtWidgets.QFileDialog.getSaveFileName()[0]
            if path:
                self.mediaObject.writeMedia(path = path)

        def setSave():
            if self.pathSourceObject:
                print(self.pathSourceObject)
                self.mediaObject.writeMedia(path=self.pathSourceObject)
                self.path = self.pathSourceObject
                self.openMedia()


        #Вызов окна выбора файла
        self.mediaQt.openAction.triggered.connect(setPath)
        self.mediaQt.addPlaylistAction.triggered.connect(setPlaylist)
        self.mediaQt.saveAction.triggered.connect(setSave)
        self.mediaQt.save_asAction.triggered.connect(setSavePath)
        self.mediaQt.exitAction.triggered.connect(self.mediaQt.close)

    def playlist(self, mode ):
        if mode == "next":
            print(self.listPlaylist)

            if 0 <= self.indexLinkPlaylist < len(self.listPlaylist) -1:
                self.indexLinkPlaylist += 1
                print("next",self.indexLinkPlaylist)
                self.path = self.listPlaylist[self.indexLinkPlaylist]
                self.openMedia()
        if mode == "back":
            if 1 <= self.indexLinkPlaylist < len(self.listPlaylist):
                self.indexLinkPlaylist -= 1
                print("back",self.indexLinkPlaylist)
                self.path = self.listPlaylist[self.indexLinkPlaylist]
                self.openMedia()


    def toolBar(self):

        '''def delete():
            self.mediaObject.deleteMedia()
            print("sa")
        try:
            print("Astart")
            self.mediaQt.actionDeleteObject.triggered.connect(delete)
            print("as")
        except: pass
        '''
        def backHistory():
            self.mediaObject.backHistoryChange()
            #self.startMedia()
            self.openMedia()
        def nextHistory():
            self.mediaObject.nextHistoryChange()
            self.openMedia()
            #self.startMedia()
        try:
            self.mediaQt.actionBackHistoryChange.triggered.connect(backHistory)
            self.mediaQt.actionNextHistoryChange.triggered.connect(nextHistory)
        except: print("Error")

try:
    import shutil
    shutil.rmtree('kesh', ignore_errors=True) #Удаление папки kesh
except: pass

try:
    os.makedirs("kesh")   #Создание папки с кешем
except FileExistsError:
    pass
app = QtWidgets.QApplication(sys.argv)
#app.installTranslator()
windowMediaWindow = MediaQt()
#windowMenuGame.setGeometry(500, 50, 640, 480)
#windowMenuGame.show()

if not app.exec_():
    import shutil
    shutil.rmtree('kesh', ignore_errors=True) #Удаление папки kesh
sys.exit(app.exec_())

