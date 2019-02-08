
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ViewerWidget(object):
    def setupUi(self, ViewerWidget):
        ViewerWidget.setObjectName("ViewerWidget")
        ViewerWidget.setEnabled(True)
        ViewerWidget.resize(700, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ViewerWidget.sizePolicy().hasHeightForWidth())
        ViewerWidget.setSizePolicy(sizePolicy)
        ViewerWidget.setMinimumSize(QtCore.QSize(700, 500))
        ViewerWidget.setMouseTracking(True)
        self.gridLayout = QtWidgets.QGridLayout(ViewerWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Layout_main = QtWidgets.QHBoxLayout()
        self.Layout_main.setObjectName("Layout_main")
        self.Layout_mainOptions = QtWidgets.QGridLayout()
        self.Layout_mainOptions.setHorizontalSpacing(2)
        self.Layout_mainOptions.setVerticalSpacing(3)
        self.Layout_mainOptions.setObjectName("Layout_mainOptions")
        self.pushButton_Connect = QtWidgets.QPushButton(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Connect.sizePolicy().hasHeightForWidth())
        self.pushButton_Connect.setSizePolicy(sizePolicy)
        self.pushButton_Connect.setMinimumSize(QtCore.QSize(100, 0))
        self.pushButton_Connect.setMaximumSize(QtCore.QSize(150, 16777215))
        self.pushButton_Connect.setObjectName("pushButton_Connect")
        self.Layout_mainOptions.addWidget(self.pushButton_Connect, 0, 2, 1, 1)
        self.Label_spectrum = QtWidgets.QLabel(ViewerWidget)
        self.Label_spectrum.setMinimumSize(QtCore.QSize(0, 10))
        self.Label_spectrum.setMaximumSize(QtCore.QSize(16777215, 20))
        self.Label_spectrum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Label_spectrum.setObjectName("Label_spectrum")
        self.Layout_mainOptions.addWidget(self.Label_spectrum, 2, 0, 1, 1)
        self.comboBox_port = QtWidgets.QComboBox(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_port.sizePolicy().hasHeightForWidth())
        self.comboBox_port.setSizePolicy(sizePolicy)
        self.comboBox_port.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBox_port.setMaximumSize(QtCore.QSize(120, 16777215))
        self.comboBox_port.setObjectName("comboBox_port")
        self.Layout_mainOptions.addWidget(self.comboBox_port, 0, 1, 1, 1)
        self.lineEdit_baudrate = QtWidgets.QLineEdit(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_baudrate.sizePolicy().hasHeightForWidth())
        self.lineEdit_baudrate.setSizePolicy(sizePolicy)
        self.lineEdit_baudrate.setMinimumSize(QtCore.QSize(120, 0))
        self.lineEdit_baudrate.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lineEdit_baudrate.setObjectName("lineEdit_baudrate")
        self.Layout_mainOptions.addWidget(self.lineEdit_baudrate, 1, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_minColor = QtWidgets.QComboBox(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_minColor.sizePolicy().hasHeightForWidth())
        self.comboBox_minColor.setSizePolicy(sizePolicy)
        self.comboBox_minColor.setMinimumSize(QtCore.QSize(55, 0))
        self.comboBox_minColor.setMaximumSize(QtCore.QSize(55, 16777215))
        self.comboBox_minColor.setObjectName("comboBox_minColor")
        self.horizontalLayout.addWidget(self.comboBox_minColor)
        self.comboBox_maxColor = QtWidgets.QComboBox(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_maxColor.sizePolicy().hasHeightForWidth())
        self.comboBox_maxColor.setSizePolicy(sizePolicy)
        self.comboBox_maxColor.setMinimumSize(QtCore.QSize(55, 0))
        self.comboBox_maxColor.setMaximumSize(QtCore.QSize(55, 16777215))
        self.comboBox_maxColor.setObjectName("comboBox_maxColor")
        self.horizontalLayout.addWidget(self.comboBox_maxColor)
        self.Layout_mainOptions.addLayout(self.horizontalLayout, 2, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_2.setSpacing(7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_maxColor = QtWidgets.QLineEdit(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maxColor.sizePolicy().hasHeightForWidth())
        self.lineEdit_maxColor.setSizePolicy(sizePolicy)
        self.lineEdit_maxColor.setMinimumSize(QtCore.QSize(55, 0))
        self.lineEdit_maxColor.setMaximumSize(QtCore.QSize(55, 16777215))
        self.lineEdit_maxColor.setObjectName("lineEdit_maxColor")
        self.horizontalLayout_2.addWidget(self.lineEdit_maxColor)
        self.lineEdit_minColor = QtWidgets.QLineEdit(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_minColor.sizePolicy().hasHeightForWidth())
        self.lineEdit_minColor.setSizePolicy(sizePolicy)
        self.lineEdit_minColor.setMinimumSize(QtCore.QSize(55, 0))
        self.lineEdit_minColor.setMaximumSize(QtCore.QSize(55, 16777215))
        self.lineEdit_minColor.setFrame(True)
        self.lineEdit_minColor.setObjectName("lineEdit_minColor")
        self.horizontalLayout_2.addWidget(self.lineEdit_minColor)
        self.Layout_mainOptions.addLayout(self.horizontalLayout_2, 2, 1, 1, 1)
        self.Label_portSelect = QtWidgets.QLabel(ViewerWidget)
        self.Label_portSelect.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_portSelect.sizePolicy().hasHeightForWidth())
        self.Label_portSelect.setSizePolicy(sizePolicy)
        self.Label_portSelect.setMinimumSize(QtCore.QSize(70, 0))
        self.Label_portSelect.setMaximumSize(QtCore.QSize(200, 20))
        self.Label_portSelect.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Label_portSelect.setObjectName("Label_portSelect")
        self.Layout_mainOptions.addWidget(self.Label_portSelect, 0, 0, 1, 1)
        self.Label_baudrate = QtWidgets.QLabel(ViewerWidget)
        self.Label_baudrate.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_baudrate.sizePolicy().hasHeightForWidth())
        self.Label_baudrate.setSizePolicy(sizePolicy)
        self.Label_baudrate.setMinimumSize(QtCore.QSize(100, 0))
        self.Label_baudrate.setMaximumSize(QtCore.QSize(200, 20))
        self.Label_baudrate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Label_baudrate.setObjectName("Label_baudrate")
        self.Layout_mainOptions.addWidget(self.Label_baudrate, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_Terminal = QtWidgets.QCheckBox(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_Terminal.sizePolicy().hasHeightForWidth())
        self.checkBox_Terminal.setSizePolicy(sizePolicy)
        self.checkBox_Terminal.setObjectName("checkBox_Terminal")
        self.horizontalLayout_3.addWidget(self.checkBox_Terminal)
        self.toolButton = QtWidgets.QToolButton(ViewerWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_3.addWidget(self.toolButton)
        self.Layout_mainOptions.addLayout(self.horizontalLayout_3, 1, 2, 1, 1)
        self.Layout_main.addLayout(self.Layout_mainOptions)
        self.terminal = QtWidgets.QTextEdit(ViewerWidget)
        self.terminal.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.terminal.sizePolicy().hasHeightForWidth())
        self.terminal.setSizePolicy(sizePolicy)
        self.terminal.setMinimumSize(QtCore.QSize(215, 0))
        self.terminal.setMaximumSize(QtCore.QSize(215, 75))
        self.terminal.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.terminal.setMouseTracking(True)
        self.terminal.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.terminal.setAcceptDrops(False)
        self.terminal.setStyleSheet("background-color: rgb(36, 36, 36);\n"
"color: rgb(226, 226, 226);\n"
"disabled {background-color: rgb(0, 0, 0); }\n"
"")
        self.terminal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.terminal.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.terminal.setLineWidth(10)
        self.terminal.setMidLineWidth(10)
        self.terminal.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.terminal.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.terminal.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.terminal.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.terminal.setTabChangesFocus(True)
        self.terminal.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        self.terminal.setReadOnly(True)
        self.terminal.setAcceptRichText(False)
        self.terminal.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.terminal.setObjectName("terminal")
        self.Layout_main.addWidget(self.terminal)
        self.Layout_terminalOptions = QtWidgets.QVBoxLayout()
        self.Layout_terminalOptions.setObjectName("Layout_terminalOptions")
        self.checkbox_Autoscroll = QtWidgets.QCheckBox(ViewerWidget)
        self.checkbox_Autoscroll.setObjectName("checkbox_Autoscroll")
        self.Layout_terminalOptions.addWidget(self.checkbox_Autoscroll)
        self.pushButton_saveTerminal = QtWidgets.QPushButton(ViewerWidget)
        self.pushButton_saveTerminal.setObjectName("pushButton_saveTerminal")
        self.Layout_terminalOptions.addWidget(self.pushButton_saveTerminal)
        self.pushButton_clearTerminal = QtWidgets.QPushButton(ViewerWidget)
        self.pushButton_clearTerminal.setObjectName("pushButton_clearTerminal")
        self.Layout_terminalOptions.addWidget(self.pushButton_clearTerminal)
        self.Layout_main.addLayout(self.Layout_terminalOptions)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.Layout_main.addItem(spacerItem)
        self.gridLayout.addLayout(self.Layout_main, 2, 5, 1, 1)
        self.widget_Mpl = MplWidget(ViewerWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(15)
        sizePolicy.setHeightForWidth(self.widget_Mpl.sizePolicy().hasHeightForWidth())
        self.widget_Mpl.setSizePolicy(sizePolicy)
        self.widget_Mpl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_Mpl.setAutoFillBackground(False)
        self.widget_Mpl.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_Mpl.setObjectName("widget_Mpl")
        self.gridLayout.addWidget(self.widget_Mpl, 3, 5, 2, 1)

        self.retranslateUi(ViewerWidget)
        QtCore.QMetaObject.connectSlotsByName(ViewerWidget)

    def retranslateUi(self, ViewerWidget):
        _translate = QtCore.QCoreApplication.translate
        ViewerWidget.setWindowTitle(_translate("ViewerWidget", "Form"))
        self.pushButton_Connect.setText(_translate("ViewerWidget", "Connect"))
        self.Label_spectrum.setText(_translate("ViewerWidget", "Color spectrum:"))
        self.Label_portSelect.setText(_translate("ViewerWidget", "Data Port:"))
        self.Label_baudrate.setText(_translate("ViewerWidget", "Baudrate:"))
        self.checkBox_Terminal.setText(_translate("ViewerWidget", "Show Terminal"))
        self.toolButton.setText(_translate("ViewerWidget", "..."))
        self.checkbox_Autoscroll.setText(_translate("ViewerWidget", "AutoScroll"))
        self.pushButton_saveTerminal.setText(_translate("ViewerWidget", "Save"))
        self.pushButton_clearTerminal.setText(_translate("ViewerWidget", "Clear"))

from mplWidget import MplWidget
