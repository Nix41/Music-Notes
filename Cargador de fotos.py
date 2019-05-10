from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QInputDialog, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog
import ctypes
from main import musical_notes
from play import play_notes
import multiprocessing as mp

if __name__ == '__main__':
    # mp.freeze_support()
    class QImageViewer(QMainWindow):
        def __init__(self):
            super().__init__()

            self.printer = QPrinter()
            self.scaleFactor = 0.0

            self.imageLabel = QLabel()
            self.imageLabel.setBackgroundRole(QPalette.Base)
            self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.imageLabel.setScaledContents(True)

            self.scrollArea = QScrollArea()
            self.scrollArea.setBackgroundRole(QPalette.Dark)
            self.scrollArea.setWidget(self.imageLabel)
            self.scrollArea.setVisible(False)

            self.setCentralWidget(self.scrollArea)
            self.createActions()
            self.createMenus()
            self.setWindowTitle("Image Viewer")
            screensize = 1200,800
            self.resize(screensize[0], screensize[1])
            #Estos aqui son los parametros a modificar en el config, les estoy poniendo valores por defecto
            self.minArea = 150
            self.maxArea = 1500
            self.set_image_size(600,800)
            self.other = 100
        def open(self):
            options = QFileDialog.Options()
            # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
            self.current_fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                    'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
            #print(self.current_fileName)
            self.show_photo(self.current_fileName)
            self.changeMaxAct.setEnabled(True)
            self.changeMinAct.setEnabled(True)
            self.changeOtherAct.setEnabled(True)
            self.play_musicAct.setEnabled(False)
            self.nextAct.setEnabled(False)
            self.star_analisisAct.setEnabled(True)
            self.updateActions()
            self.set_image_size(600,800)
            #self.get_result_photos()    
            #self.lastAct.setEnabled(False)
            #self.nextAct.setEnabled(True)
            #self.printAct.setEnabled(True)
            #self.updateActions()
            
        def star_analisis(self):
            #Metodo en que corres tu analisis con los parametros actuales, tienes que guardar en self.all_photos los path de las fotos del resultado
            try:
                self.notes = musical_notes(self.current_fileName, self.minArea, self.maxArea)
            except Exception:
                print('La imagen no se pudo analizar')
            #En self.current_fileName esta el path de la foto que el tipo selecciono 
            self.index_of_photo = 0 # indice de foto actual en la que estamos parados
            self.all_photos = []
            #DO ALGO PARA CARGAR LAS FOTOS Y PONERLAS A CORRER. Lo que hay que hacer es anadir el path de los result a all_photos
            self.all_photos.append("output/1canny.jpg")                
            self.all_photos.append("output/2with_contours.png")
            self.all_photos.append("output/5lines.png")
            self.all_photos.append("output/8a_lines_horizontal_removed.png")
            self.all_photos.append("output/8a_lines_vertical_removed.png")
            self.all_photos.append("output/8b_with_blobs.jpg")
            self.all_photos.append("output/8c_with_numbers.jpg")
            self.all_photos.append("output/8d_with_staff_numbers.jpg")
            self.all_photos.append("output/9_with_pitch.png")
            self.show_photo(self.all_photos[self.index_of_photo]) #Aqui ensenno la primera foto
            self.set_image_size(600,800)
            #poner visibles estas acciones
            self.lastAct.setEnabled(False)
            self.nextAct.setEnabled(True)
            self.printAct.setEnabled(True)
            self.play_musicAct.setEnabled(True)
            self.updateActions()
            
        def play_song(self):
            #Metodo donde corres la cancion
            self.stop_musicAct.setEnabled(True)
            self.current_process = mp.Process(target= play_notes, args=(self.notes,))
            self.current_process.start()
            print('here')
        
        def stop_song(self):
            self.current_process.terminate()
            self.stop_musicAct.setEnabled(False)

        
        def show_photo(self,fileName):
            if fileName:
                image = QImage(fileName)
                if image.isNull():
                    QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                    return

                self.imageLabel.setPixmap(QPixmap.fromImage(image))
                self.scaleFactor = 1.0
                self.scrollArea.setVisible(True)
                
                self.fitToWindowAct.setEnabled(True)
                self.updateActions()
                if not self.fitToWindowAct.isChecked():
                    self.set_image_size(600,800)

        def getInteger(self,name,nameOfvariable,default,mini,maxi,step):
            #Metodo que abre una ventada de entrada con las variables de entrada
            i, okPressed = QInputDialog.getInt(self, name,nameOfvariable, default, mini, maxi, step)
            if okPressed:
                return i
            else:
                return -1
        def change_min_value(self):
            temp = self.getInteger("Change Minimun Area of Blob", "MinimunA", self.minArea, 0,self.maxArea, 1)
            if temp != -1:
                self.minArea = temp
        def change_max_value(self):
            temp = self.getInteger("Change Maximun Area of Blob", "MaximoA", self.maxArea, self.minArea, 5000, 1)
            if temp != -1:
                self.maxArea = temp
        def change_other_parametro(self):
            #Aqui tienes que cambiarle el nombre, nombre, valor predeterminado, minimo,maximo, y step
            #Todo ver segun el parametro que cosa es el nombre que le vas a poner al dialogo, los maximos y minimos y tal
            temp = self.getInteger("Change The other parametro", "other", self.other, 0, 500, 1)
            if temp != -1:
                self.other = temp
        
        def next_photo(self):
            #Mueve para la siguiente foto
            if self.index_of_photo < len(self.all_photos) -1:
                self.index_of_photo +=1
                self.show_photo(self.all_photos[self.index_of_photo])
            if self.index_of_photo == len(self.all_photos) -1:
                self.nextAct.setEnabled(False)
            
            if len(self.all_photos) > 1:
                self.lastAct.setEnabled(True)
            self.updateActions()
        def last_photo(self):
            #Retrosede a la anterior foto
            if self.index_of_photo > 0:
                self.index_of_photo -=1
                self.show_photo(self.all_photos[self.index_of_photo])

            if self.index_of_photo == 0:
                self.lastAct.setEnabled(False)
            self.nextAct.setEnabled(True)
            self.updateActions()
        def print_(self):
            dialog = QPrintDialog(self.printer, self)
            if dialog.exec_():
                painter = QPainter(self.printer)
                rect = painter.viewport()
                size = self.imageLabel.pixmap().size()
                size.scale(rect.size(), Qt.KeepAspectRatio)
                painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
                painter.setWindow(self.imageLabel.pixmap().rect())
                painter.drawPixmap(0, 0, self.imageLabel.pixmap())

        def zoomIn(self):
            self.scaleImage(1.25)

        def zoomOut(self):
            self.scaleImage(0.8)

        def normalSize(self):
            self.imageLabel.adjustSize()
            self.scaleFactor = 1.0
            self.set_image_size(600,800)

        def fitToWindow(self):
            fitToWindow = self.fitToWindowAct.isChecked()
            # self.scrollArea.setWidgetResizable(fitToWindow)
            if not fitToWindow:
                self.normalSize()
            self.set_image_size(600,800)
            self.updateActions()
            self.set_image_size(600,800)


        def about(self):
            QMessageBox.about(self, "Lector de Partituras",
                            "Se aceptan tanto fotos de partituras, como imagenes limpias de partituras "
                            "<p>Para el <b>correcto funcionamiento </b> de este programa "
                            "Las imagenes de las partituras deben cumplir ciertos requerimientos:<br>"
                            "    Deben tener una buena resolucion, las lineas lo mas nitidas posibles<br>"
                            "    Preferiblemente no debe de haber simbolos junto a las claves que inician los pentagramas<br>"
                            "    Las notas de 2 y 4 tiempos no seran reconocidas</p>"
                            "<p>Para procesar una imagen, primero debe abrirla, usando el menu de Actions.. "
                            "<br>Luego, para analizar la partitura, tambien se usa un submenu de Actions.. "
                            "<br> El analisis de las partituras conlleva un proceso que se podra observar, navegando "
                            "a traves de los resultados, ya sea usando (ctrl+N,ctrl+P), o el menu de Actions..<br>"
                            "El analisis debe ser calibrado, teniendo en cuenta el area minima de el blob que constituye una nota "
                            "que puede variar con respecto a la resolucion de la imagen, o a su tamanno<br> "
                            "Si en la imagen final de analisis, se reconocen muchas cosas que no son notas, se cambia en menu de Action.."
                            "y Se aumenta el area minima para las notas<br> "
                            "Si por el contrario, no se reconocen todas tamannolas notas, de debe bajar el area minima<br>"
                            "Para el zoom de las imagenes se puede usar (ctrl+, ctrl-) o el submenu de View..<br>"
                            "Una vez que este complacido con el analisis de la partitura, encontrara bajo el menu de Action.."
                            "Una opcion para reproducir la partitura reconocida<br>"
                            "ADVERTENCIA!! Si la partitura no es reconocida correctamente, la reproduccion puede volverse bstante desgradable al oido"
                            "ADVERTENCIA!! Los pentagramas se leeran de forma continua, como un solo instrumento "
                            ", para que la reproduccion sea lo mas fiel posible, se deben escoger partituras que esten hechas con dicha intencion</p>")

        def createActions(self):
            self.openAct = QAction("&Open...", self, shortcut="Ctrl+O", triggered=self.open)
            self.printAct = QAction("&Print...", self, shortcut="Ctrl+E", enabled=False, triggered=self.print_)
            self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=self.close)
            self.zoomInAct = QAction("Zoom &In (25%)", self, shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)
            
            self.zoomOutAct = QAction("Zoom &Out (25%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)
            self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)
            self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False, checkable=True, shortcut="Ctrl+F",
                                        triggered=self.fitToWindow)
            self.fitToWindowAct.setChecked(True)
            self.fitToWindow()
            self.nextAct = QAction("&Next photo",self,enabled = False,checkable = False,shortcut = "Ctrl+N", triggered = self.next_photo)
            self.lastAct = QAction("&Previous photo",self,enabled = False,checkable = False,shortcut = "Ctrl+P", triggered = self.last_photo)
            
            self.changeMinAct = QAction("&Change Minimun Area", self,enabled = False,checkable = False,shortcut = "Ctrl+A", triggered = self.change_min_value )
            self.changeMaxAct = QAction("&Change Maximun Area", self,enabled = False,checkable = False,shortcut = "Ctrl+B", triggered = self.change_max_value )
            self.changeOtherAct = QAction("&Change Other", self,enabled = False,checkable = False,shortcut = "Ctrl+C", triggered = self.change_other_parametro )
            
            self.star_analisisAct = QAction("&Run Analisis", self,enabled = False,checkable = False,shortcut = "Ctrl+F", triggered = self.star_analisis)
            self.play_musicAct = QAction("&Play Music", self,enabled = False,checkable = False,shortcut = "Ctrl+L", triggered = self.play_song)
            self.stop_musicAct = QAction("&Stop Music", self,enabled = False,checkable = False,shortcut = "Ctrl+K", triggered = self.stop_song)

            self.aboutAct = QAction("&About", self, triggered=self.about)
            self.aboutQtAct = QAction("About &Qt", self, triggered=qApp.aboutQt)

        def createMenus(self):
            self.fileMenu = QMenu("&Actions", self)
            self.fileMenu.addAction(self.openAct)
            #self.fileMenu.addAction(self.printAct)
            self.fileMenu.addAction(self.nextAct)
            self.fileMenu.addAction(self.lastAct)
            
            self.fileMenu.addAction(self.changeMinAct)
            self.fileMenu.addAction(self.changeMaxAct)
            self.fileMenu.addAction(self.changeOtherAct)
            
            self.fileMenu.addAction(self.star_analisisAct)
            self.fileMenu.addAction(self.play_musicAct)
            self.fileMenu.addAction(self.stop_musicAct)

            self.fileMenu.addSeparator()
            self.fileMenu.addAction(self.exitAct) 

            self.viewMenu = QMenu("&View", self)
            self.viewMenu.addAction(self.zoomInAct)
            self.viewMenu.addAction(self.zoomOutAct)
            self.viewMenu.addAction(self.normalSizeAct)
            self.viewMenu.addSeparator()
            self.viewMenu.addAction(self.fitToWindowAct)

            self.helpMenu = QMenu("&Help", self)
            self.helpMenu.addAction(self.aboutAct)
            self.helpMenu.addAction(self.aboutQtAct)

            self.menuBar().addMenu(self.fileMenu)
            self.menuBar().addMenu(self.viewMenu)
            self.menuBar().addMenu(self.helpMenu)

        def updateActions(self):
            self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
            self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
            self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

        def scaleImage(self, factor):
            self.scaleFactor *= factor
            self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

            self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
            self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

            self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
            self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

        def adjustScrollBar(self, scrollBar, factor):
            scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep() / 2)))
        def set_image_size(self,n, m):
            self.imageLabel.resize(n,m)
            self.scrollArea.horizontalScrollBar().setValue(n)
            self.scrollArea.verticalScrollBar().setValue(m)

    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    imageViewer = QImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
# TODO QScrollArea support mouse