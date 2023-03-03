# import PyQt5.QtWidgets as qtw
# import PyQt5.QtGui as qtg
from classes.engToImage import Stability

font = "Verdana"
stab = Stability()


def engToImg(str):
    stab.generateImage(str)


# --------------------------------------------- test --------------------------------------------

# engToImg("green cats ")

# class MainWindow(qtw.QWidget) :
#     def __init__(self):
#         super().__init__()

#         stab = Stability()

#         self.setWindowTitle("Stability test")
#         self.setLayout(qtw.QVBoxLayout())
#         # self.setFixedWidth(512)
#         # self.setFixedHeight(600)

#         my_label = qtw.QLabel("Type in the text")
#         my_label.setFont(qtg.QFont(font, 20))
#         my_label.move(0, 0)
#         self.layout().addWidget(my_label)

#         text_input = qtw.QLineEdit(self,
#             # lineWrapMode=qtw.QLineEdit.FixedColumnWidth,
#             # lineWrapColumnOrWidth=50,
#             placeholderText="expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli",
#             readOnly = False
#             )
#         text_input.setObjectName("input for bot")
#         text_input.setText("")
#         text_input.setFont(qtg.QFont(font, 16))
#         text_input.move(0, 24)
#         self.layout().addWidget(text_input)

#         button = qtw.QPushButton("generate",
#             clicked = lambda: outputImage()
#             )
#         self.layout().addWidget(button)

#         image_zone = qtw.QLabel(self)
#         image_zone.move(0, 44)

#         self.show()

#         def outputImage() :
#             seed = text_input.text()
#             if (seed == "") :
#                 seed = text_input.placeholderText()
#             image = stab.generateImage(seed)
#             pixmap = qtg.QPixmap(image)
#             # image_zone = qtw.QHBoxLayout()
#             # first_image = qtw.QLabel(self)
#             # second_image = qtw.QLabel(self)
#             # first_image.setPixmap(pixmap)
#             # second_image.setPixmap(pixmap)
#             image_zone.setPixmap(pixmap)

#             # image_zone.addWidget(first_image)
#             # image_zone.addWidget(second_image)
#             self.layout().addWidget(image_zone)
#             # self.resize(pixmap.width(), pixmap.height())


# app = qtw.QApplication([])
# mw = MainWindow()

# app.exec_()


# app = Stability()

# app.generateImage("expansive landscape rolling greens with blue daisies and weeping willow trees under a blue alien sky, artstation, masterful, ghibli").show()
