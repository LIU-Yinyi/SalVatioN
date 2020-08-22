from . import svn


class App:
    def __init__(self):
        self.bundle_db = None

    from .win_bundlelist import setup_ui_bundle, \
        event_listwidget_repos_right_click, event_listwidget_repos_left_click, \
        event_listwidget_repos_menu_add, event_listwidget_repos_menu_edit,\
        event_listwidget_repos_menu_delete, event_listwidget_repos_menu_duplicate, \
        event_listwidget_repos_menu_connect, event_listwidget_repos_menu_refresh

    from .win_repoconfig import setup_ui_repoconfig, \
        event_button_login_by_password, event_button_login_by_sshkey, \
        event_button_load_sshkey, event_lineedit_address_onchange

