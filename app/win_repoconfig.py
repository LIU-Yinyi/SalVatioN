import re
from PyQt5.QtWidgets import QFileDialog

from . import db_bundlelist


def setup_ui_repoconfig(self):
    self.ui.comboBox_logo.addItem('Default')
    self.ui.checkBox_configssh.setChecked(False)


def event_button_login_by_password(self):
    _username = self.ui.lineEdit_username.text()
    _password = self.ui.lineEdit_password.text()
    _address = self.ui.lineEdit_address.text()
    if self.svn.login(username=_username, password=_password, address=_address):
        func_login_success_save_config(self)
    else:
        self.ui.statusbar.showMessage('[Error] Wrong Password.', 5000)


def event_button_login_by_sshkey(self):
    _username = self.ui.lineEdit_username.text()
    _sshkey = self.ui.lineEdit_sshkey.text()
    _address = self.ui.lineEdit_address.text()
    if self.svn.login(username=_username, sshkey=_sshkey, address=_address):
        func_login_success_save_config(self)
    else:
        self.ui.statusbar.showMessage('[Error] Wrong SSH-Hey.', 5000)


def event_button_load_sshkey(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    sshfile, _ = QFileDialog.getOpenFileName(self, "Select SSH-Key File", "", "Sshkey Files (*)", options=options)
    if sshfile:
        self.ui.lineEdit_sshkey.setText(sshfile)


def event_lineedit_address_onchange(self):
    self.ui.lineEdit_alias.setText(re.split('/|\.', self.ui.lineEdit_address.text())[0])


def func_login_success_save_config(self):
    cfg = self.svn.get_config()
    cfg['alias'] = self.ui.lineEdit_alias.text()
    cfg['autocfg'] = self.ui.checkBox_configssh.isChecked()
    db_bundlelist.save_bundle(cfg)
    self.ui.statusbar.showMessage('[Info] Connected & Saved.', 5000)
    self.setup_ui_bundle()

