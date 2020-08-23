import sys
import app
import gui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication


class Salvation(QMainWindow, app.App):
    def __init__(self):
        super().__init__()
        self.svn = app.svn.Client()
        self.ui = gui.ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setup_ui()
        self.register_ui_event()

    def setup_ui(self):
        self.setup_ui_statusbar()
        self.setup_ui_bundle()
        self.setup_ui_repoconfig()
        self.setup_ui_remotesvn()
        self.ui.statusbar.showMessage("[Welcome] Powered by LIU-Yinyi :D")

    def register_ui_event(self):
        # win_bundlelist
        self.ui.listWidget_repos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget_repos.customContextMenuRequested.connect(self.event_listwidget_repos_right_click)
        self.ui.listWidget_repos.mousePressEvent = self.event_listwidget_repos_left_click
        # win_reposconfig
        self.ui.pushButton_loginPassword.clicked.connect(self.event_button_login_by_password)
        self.ui.pushButton_loginKey.clicked.connect(self.event_button_login_by_sshkey)
        self.ui.pushButton_loadKey.clicked.connect(self.event_button_load_sshkey)
        self.ui.lineEdit_address.textChanged.connect(self.event_lineedit_address_onchange)
        # win_remotesvn
        self.ui.treeView_remoteSvn.setExpandsOnDoubleClick(False)  # avoid expanding twice
        self.ui.treeView_remoteSvn.mousePressEvent = self.event_remotesvn_treeview_left_click
        self.ui.treeView_remoteSvn.mouseDoubleClickEvent = self.event_remotesvn_treeview_left_double_click
        self.ui.treeView_remoteSvn.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeView_remoteSvn.customContextMenuRequested.connect(self.event_remotesvn_treeview_right_click)


if __name__ == '__main__':
    application = QApplication(sys.argv)
    windows = Salvation()
    windows.show()
    sys.exit(application.exec_())
