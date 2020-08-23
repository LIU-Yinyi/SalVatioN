from . import svn
from .win_remotesvn import func_model_create

class App:
    def __init__(self):
        self._version_ = '0.1.0'
        self.bundle_db = None
        self.remotesvn_mdl = func_model_create()

    from .win_statusbar import setup_ui_statusbar, event_button_about_click

    from .win_bundlelist import setup_ui_bundle, \
        event_listwidget_repos_right_click, event_listwidget_repos_left_click, \
        event_listwidget_repos_menu_add, event_listwidget_repos_menu_edit,\
        event_listwidget_repos_menu_delete, event_listwidget_repos_menu_duplicate, \
        event_listwidget_repos_menu_connect, event_listwidget_repos_menu_refresh

    from .win_repoconfig import setup_ui_repoconfig, \
        event_button_login_by_password, event_button_login_by_sshkey, \
        event_button_load_sshkey, event_lineedit_address_onchange

    from .win_remotesvn import setup_ui_remotesvn, event_remotesvn_model_refresh, \
        event_remotesvn_treeview_left_click, \
        event_remotesvn_treeview_render, event_remotesvn_connected
