from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QListWidgetItem
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox
from PyQt5.QtGui import QFont, QColor

from . import db_bundlelist


class BundleItem(QWidget):
    def __init__(self):
        super().__init__()
        self.text_layout = QVBoxLayout()
        self.text_alias = QLabel()
        self.text_url = QLabel()
        self.text_layout.addWidget(self.text_alias)
        self.text_layout.addWidget(self.text_url)
        self.setLayout(self.text_layout)
        font_alias = QFont('Arial', 14)
        font_alias.setBold(True)
        font_url = QFont('Arial', 9)
        font_url.setBold(False)
        self.text_alias.setFont(font_alias)
        self.text_url.setFont(font_url)

    def set_text(self, alias, url):
        self.text_alias.setText(alias)
        self.text_url.setText(url)


def menu_action(txt, func, tip=None):
    action = QAction(txt)
    action.triggered.connect(func)
    if tip:
        action.setStatusTip(tip)
    return action


def setup_ui_bundle(self):
    self.ui.listWidget_repos.clear()
    event_load_bundle_config(self)
    for record in self.bundle_db:
        item = BundleItem()
        item.set_text(record[1], "{}@{}".format(record[2], record[5].split('/')[0]))
        lwitem = QListWidgetItem(self.ui.listWidget_repos)
        lwitem.setSizeHint(item.sizeHint())
        self.ui.listWidget_repos.addItem(lwitem)
        self.ui.listWidget_repos.setItemWidget(lwitem, item)


def event_load_bundle_config(self):
    self.bundle_db = db_bundlelist.load_bundle()


def event_listwidget_repos_menu_add(self):
    self.ui.lineEdit_username.setText("")
    self.ui.lineEdit_address.setText("")
    self.ui.lineEdit_alias.setText("")
    self.ui.lineEdit_password.setText("")
    self.ui.lineEdit_sshkey.setText("")
    self.ui.checkBox_configssh.setChecked(False)
    self.ui.lineEdit_username.setFocus()


def event_listwidget_repos_menu_edit(self):
    indices = self.ui.listWidget_repos.selectedIndexes()
    if len(indices) > 0:
        _id = indices[0].row()
        record = self.bundle_db[_id]
        self.ui.lineEdit_username.setText(record[2])
        self.ui.lineEdit_password.setText(record[3])
        self.ui.lineEdit_sshkey.setText(record[4])
        self.ui.lineEdit_address.setText(record[5])
        self.ui.lineEdit_alias.setText(record[1])
        self.ui.checkBox_configssh.setChecked(True if record[6] else False)
        if record[3] != "":
            self.ui.tabWidget_login.setCurrentIndex(0)
        else:
            self.ui.tabWidget_login.setCurrentIndex(1)


def event_listwidget_repos_menu_delete(self):
    indices = self.ui.listWidget_repos.selectedIndexes()
    if len(indices) > 0:
        _id = indices[0].row()
        record = self.bundle_db[_id]
        reply = QMessageBox.question(self, "Confirm Delete", "Username: {}\nAddress: {}".format(record[2], record[5]))
        if reply == QMessageBox.Yes:
            db_bundlelist.delete_bundle(id=record[0], username=record[2], address=record[5])
            self.ui.statusbar.showMessage('[Info] Bundle Deleted.', 5000)
            self.setup_ui_bundle()
        else:
            self.ui.statusbar.showMessage('[Info] Deletion Canceled.', 5000)


def event_listwidget_repos_menu_duplicate(self):
    indices = self.ui.listWidget_repos.selectedIndexes()
    if len(indices) > 0:
        _id = indices[0].row()
        record = self.bundle_db[_id]
        self.ui.lineEdit_username.setText("")
        self.ui.lineEdit_username.setFocus()
        self.ui.lineEdit_password.setText("")
        self.ui.lineEdit_sshkey.setText("")
        self.ui.lineEdit_address.setText(record[5])
        self.ui.lineEdit_alias.setText(record[1])
        self.ui.checkBox_configssh.setChecked(True if record[6] else False)
        self.ui.statusbar.showMessage('[Info] Same User will be combined', 5000)


def event_listwidget_repos_menu_connect(self):
    indices = self.ui.listWidget_repos.selectedIndexes()
    if len(indices) > 0:
        _id = indices[0].row()
        record = self.bundle_db[_id]
        self.ui.statusbar.showMessage("[Info] Connecting to {}...".format(record[1]))
        if self.svn.login(username=record[2], password=record[3], sshkey=record[4], address=record[5], remain=False):
            self.event_remotesvn_connected()
            self.ui.statusbar.showMessage('[Info] Connected successfully.', 5000)
        else:
            self.ui.statusbar.showMessage('[Info] Connection failed.', 5000)


def event_listwidget_repos_menu_refresh(self):
    self.setup_ui_bundle()
    self.ui.statusbar.showMessage('[Info] Bundle Refreshed.', 5000)


def event_listwidget_repos_right_click(self, pos):
    indices = self.ui.listWidget_repos.selectedIndexes()
    menu = QMenu()
    act_add = menu_action('Add', self.event_listwidget_repos_menu_add)
    menu.addAction(act_add)

    if len(indices) > 0:
        act_edit = menu_action('Edit', self.event_listwidget_repos_menu_edit)
        act_delete = menu_action('Delete', self.event_listwidget_repos_menu_delete)
        act_duplicate = menu_action('Duplicate', self.event_listwidget_repos_menu_duplicate)
        act_connect = menu_action('Connect', self.event_listwidget_repos_menu_connect)

        menu.addAction(act_edit)
        menu.addAction(act_delete)
        menu.addAction(act_duplicate)
        menu.addSeparator()
        menu.addAction(act_connect)

    act_refresh = menu_action('Refresh', self.event_listwidget_repos_menu_refresh)
    menu.addSeparator()
    menu.addAction(act_refresh)

    menu.exec_(self.ui.listWidget_repos.viewport().mapToGlobal(pos))


def event_listwidget_repos_left_click(self, event):
    _index = self.ui.listWidget_repos.indexAt(event.pos())
    if _index.isValid():
        self.ui.listWidget_repos.setCurrentIndex(_index)
    else:
        self.ui.listWidget_repos.clearSelection()
