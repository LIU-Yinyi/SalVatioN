from PyQt5.QtWidgets import QLabel, QMessageBox


ABOUT_HEADER = '''
SalVatioN is a open-source SVN-GUI Project.
Powered by @LIU-Yinyi (C) 2020

[Version] {}
[Website] https://github.com/LIU-Yinyi/SalVatioN.git
'''

ABOUT_MESSAGE = "\
[Motivation]\n\
This project was originally for Yinyi's Macbook because \
at that time MacOSX Catalina didn't have relevant soft \
that could support free subversion desktop version. But \
the lab duty required svn so I wrote a gui version as \
SALVATION. It happened that the word 'salvation' has the \
letter 'svn', as a result, I named the software as it :D \
"


def setup_ui_statusbar(self):
    _about = QLabel('About')
    _about.mousePressEvent = self.event_button_about_click
    _about.setStyleSheet("border-bottom-width: 1px; border-bottom-style: solid; border-radius: 0px;")
    self.ui.statusbar.addPermanentWidget(_about)


def event_button_about_click(self, event):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("About SalVatioN")
    msg.setText(ABOUT_HEADER.format(self._version_))
    msg.setInformativeText(ABOUT_MESSAGE)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

