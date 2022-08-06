from highlight import PSNR, cropd_img
from extract2 import extract_img_embd
from insert2 import insert_img_embd
from os import path
from PyQt5.QtWidgets import QMessageBox
from gui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from insert import insrt, rgb_insrt
from extract import dtct, extrct, rgb_dctct, rgb_extract
from PIL import Image


img_path = "imgs/def.svg"
lg_path = "imgs/log_img.svg"
act = 1
ps = 0.0

class Inter(QtWidgets.QMainWindow):

    
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.res_bttn.hide()
        self.ui.mdf_bttn.hide()
        self.ui.img_lg.hide()
        self.ui.lg_label.hide()
        self.ui.browse_lg.hide()


        # Self Embedding - - -
        self.ui.ins_sf.clicked.connect(self.sf_embd)

        self.ui.extr_sf.clicked.connect(self.sf_extrct)

        # browse files 
        self.ui.browse.clicked.connect(self.browsefiles)

        # start insertion / extraction 
        self.ui.start.clicked.connect(self.start_ie)

        # extracted image 
        self.ui.res_bttn.clicked.connect(self.ext_sf)

        # highlighted modified image
        self.ui.mdf_bttn.clicked.connect(self.mdf_sf)

        # Image Embedding - - -

        self.ui.ins_lsb.clicked.connect(self.lsb_embd)

        self.ui.extr_lsb.clicked.connect(self.lsb_extrct)

        # browse logos
        self.ui.browse_lg.clicked.connect(self.browselg)

        # calcul psnr

        self.ui.psnr_bttn.clicked.connect(self.cal_psnr)



        # about
        self.ui.abt.clicked.connect(self.about)
        
    
    def sf_embd(self):
        global act
        global img_path
        
        act = 1
        # Refresh
        self.ui.res_bttn.hide()
        self.ui.mdf_bttn.hide()
        self.ui.img_lg.hide()
        self.ui.lg_label.hide()
        self.ui.browse_lg.hide()
        self.ui.img_dst.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.img_src.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.keyf.clear()
        self.ui.psnr_f.clear()
        self.ui.phase.setText("Self-Embedding - Embed Phase")
        img_path = "imgs/def.svg"

        

    def sf_extrct(self):
        global act
        global img_path

        act = 2
        # Refresh
        self.ui.res_bttn.show()
        self.ui.mdf_bttn.show()
        self.ui.psnr_f.show()
        self.ui.psnr_bttn.show()
        self.ui.img_lg.hide()
        self.ui.lg_label.hide()
        self.ui.browse_lg.hide()
        self.ui.img_dst.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.img_src.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.keyf.clear()
        self.ui.psnr_f.clear()
        self.ui.phase.setText("Self-Embedding - Extract Phase")
        img_path = "imgs/def.svg"


    def lsb_embd(self):
        global act
        global img_path
        global lg_path
        
        act = 3
        # Refresh
        self.ui.res_bttn.hide()
        self.ui.mdf_bttn.hide()
        self.ui.img_dst.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.img_src.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.img_lg.setPixmap(QtGui.QPixmap("imgs/log_img.svg"))
        self.ui.keyf.clear()
        self.ui.phase.setText("Image-Embedding - Embed Phase")
        img_path = "imgs/def.svg"
        lg_path = "imgs/log_img.svg"
        

    def lsb_extrct(self):
        global act
        global img_path
        global lg_path
        
        act = 4
        # Refresh
        self.ui.psnr_f.show()
        self.ui.psnr_bttn.show()
        self.ui.res_bttn.show()
        self.ui.mdf_bttn.show()
        self.ui.img_dst.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.img_src.setPixmap(QtGui.QPixmap("imgs/def.svg"))
        self.ui.keyf.clear()
        self.ui.phase.setText("Image-Embedding - Extract Phase")
        img_path = "imgs/def.svg"
        lg_path = "imgs/log_img.svg"



    def browsefiles(self):
        global img_path
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'image', 'Images (*.png *.jpg *.bmp)')
        if file_name[0] != '':
            self.ui.img_src.setPixmap(QtGui.QPixmap(file_name[0]))
            img_path = file_name[0]
        else:
            self.ui.img_src.setPixmap(QtGui.QPixmap("imgs/def.svg"))
            img_path = "imgs/def.svg"
    
    def browselg(self):
        global lg_path
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'image', 'Images (*.png *.jpg *.bmp)')
        if file_name[0] != '':
            self.ui.img_lg.setPixmap(QtGui.QPixmap(file_name[0]))
            lg_path = file_name[0]
        else:
            self.ui.img_lg.setPixmap(QtGui.QPixmap("imgs/def.svg"))
            lg_path = "imgs/log_img.svg"

    def start_ie(self):
        global img_path
        global lg_path
        global ps
        # insertion self-embedding
        
        if act == 1:
            key = self.ui.keyf.text()
            if not str.isdecimal(key):
                QtWidgets.QMessageBox.critical(self, 'ERR', 'clé non valide')
            else:
                if img_path == "imgs/def.svg":
                    QtWidgets.QMessageBox.critical(self, 'ERR', 'sélectionner une image')
                else:
                    x, y = Image.open(img_path).size
                    if x % 8 != 0 or y % 8 != 0:
                        request = QMessageBox.information(self, "Info", "Taille de l'image non valide voulez-vous la redimensionner ?",QMessageBox.No | QMessageBox.Yes )
                        if request == 16384:

                            rgb_insrt(img_path, key)

                            tmp_pth = "tmp"+img_path[-4:]
                            output = open(tmp_pth, "wb")
                            im  = Image.open(img_path)
                            im = cropd_img(im)
                            im.save(output)
                            ps = PSNR(tmp_pth,'img_watermarked/wtrmrkd.png')
                            if path.exists('img_watermarked/wtrmrkd.png'):
                                self.ui.img_dst.setPixmap(QtGui.QPixmap("img_watermarked/wtrmrkd.png"))
                            else:
                                QtWidgets.QMessageBox.critical(self, 'ERROR', 'Erreur d\'insertion')
                        else:
                            self.ui.img_src.setPixmap(QtGui.QPixmap("imgs/def.svg"))
                            img_path = "imgs/def.svg"
                    else:
                        rgb_insrt(img_path, key)
                        ps = PSNR(img_path,'img_watermarked/wtrmrkd.png')
                        if path.exists('img_watermarked/wtrmrkd.png'):
                            self.ui.img_dst.setPixmap(QtGui.QPixmap("img_watermarked/wtrmrkd.png"))
                        else:
                            QtWidgets.QMessageBox.critical(self, 'ERROR', 'Erreur d\'insertion')
        
        # extraction self-embedding
        if act == 2:
            key = self.ui.keyf.text()
            if not str.isdecimal(key):
                QtWidgets.QMessageBox.critical(self, 'ERR', 'clé non valide')
            else:
                if img_path == "imgs/def.svg":
                    QtWidgets.QMessageBox.critical(self, 'ERR', 'sélectionner une image')
                else:
                    
                    rgb_extract(img_path,key)
                    rgb_dctct(img_path,key)
                
                    tmp_pth = "tmp"+img_path[-4:]
                    output = open(tmp_pth, "wb")
                    im  = Image.open(img_path)
                    im = cropd_img(im)
                    im.save(output)
                    ps = PSNR(tmp_pth,"img_resultats/res.png")
                    if path.exists('img_resultats/res.png'):
                        self.ext_sf()
                    else:
                        QtWidgets.QMessageBox.critical(self, 'ERROR', 'Erreur d\'extraction')

        # insertion image-embedding

        if act == 3:
            key = self.ui.keyf.text()
            if not str.isdecimal(key):
                QtWidgets.QMessageBox.critical(self, 'ERR', 'clé non valide')
            else:
                if img_path == "imgs/def.svg":
                    QtWidgets.QMessageBox.critical(self, 'ERR', 'sélectionner une image')
                else:
                    x, y = Image.open(img_path).size
                    if x % 8 != 0 or y % 8 != 0:
                        request = QMessageBox.information(self, "Info", "Taille de l'image non valide voulez-vous la redimensionner ?",QMessageBox.No | QMessageBox.Yes )
                        if request == 16384:
                            insert_img_embd(img_path, key)
                            tmp_pth = "tmp"+img_path[-4:]
                            output = open(tmp_pth, "wb")
                            im  = Image.open(img_path)
                            im = cropd_img(im)
                            im.save(output)
                            ps = PSNR(tmp_pth,"img_watermarked/wtrmrkd_by_img.png")
                            
                            self.ui.img_dst.setPixmap(QtGui.QPixmap("img_watermarked/wtrmrkd_by_img.png"))
                        else:
                            self.ui.img_src.setPixmap(QtGui.QPixmap("imgs/def.svg"))
                            img_path = "imgs/def.svg"
                    else:
                        insert_img_embd(img_path, key)
                        ps = PSNR(img_path,"img_watermarked/wtrmrkd_by_img.png")
                        self.ui.img_dst.setPixmap(QtGui.QPixmap("img_watermarked/wtrmrkd_by_img.png"))
                                
                           
        
        # extraction image-embedding
        if act == 4:
            key = self.ui.keyf.text()
            if not str.isdecimal(key):
                QtWidgets.QMessageBox.critical(self, 'ERR', 'clé non valide')
            else:
                if img_path == "imgs/def.svg":
                    QtWidgets.QMessageBox.critical(self, 'ERR', 'sélectionner une image')
                else:
                    extract_img_embd(img_path,key)
                    ps = PSNR(img_path,"img_resultats/extrctd_from_img.png")
                    if path.exists("img_resultats/extrctd_from_img.png"):
                        self.ui.img_dst.setPixmap(QtGui.QPixmap("img_resultats/extrctd_from_img.png"))
                    else:
                        QtWidgets.QMessageBox.critical(self, 'ERROR', 'Erreur d\'extraction')
                        

    def cal_psnr(self):
        global ps
        self.ui.psnr_f.setText(str(ps) + " dB")

        
    
    def ext_sf(self):
        self.ui.res_bttn.setStyleSheet("QPushButton { color: rgb(255, 255, 255);background-color: rgb(233, 69, 96); border-radius: 8px}")
        self.ui.mdf_bttn.setStyleSheet("QPushButton { color: rgb(73, 84, 100); background-color: rgb(187, 191, 202); border-radius: 8px}")
        if path.exists('img_resultats/res.png'):
                        self.ui.img_dst.setPixmap(QtGui.QPixmap("img_resultats/res.png"))
    
    def mdf_sf(self):
        self.ui.mdf_bttn.setStyleSheet("QPushButton { color: rgb(255, 255, 255);background-color: rgb(233, 69, 96); border-radius: 8px}")
        self.ui.res_bttn.setStyleSheet("QPushButton { color: rgb(73, 84, 100); background-color: rgb(187, 191, 202); border-radius: 8px}")
        if path.exists('img_resultats/highlighted.png'):
                        self.ui.img_dst.setPixmap(QtGui.QPixmap("img_resultats/highlighted.png"))


    def about(self):
        QMessageBox.information(self,"About","Application de tatouage numérique par :\nAhmane Mohamed Amine et Azzouz Mouhammed Soheyb\nsous la supervision de Mme bellala",QMessageBox.Ok)
        
        



        

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Inter()
    window.setWindowTitle("Digital Watermarking App")
    window.setWindowIcon(QtGui.QIcon('icons/window_icon.png'))
    window.show()

    app.exec_()