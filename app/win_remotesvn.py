import re
from enum import IntEnum
from PyQt5.Qt import QStandardItem, QStandardItemModel
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QMenu

from .utils import menu_action


class ModelColumn(IntEnum):
    Files = 0
    Size = 1
    Status = 2
    Version = 3
    Author = 4
    ChangedDate = 5


class ModelItem(QStandardItem):
    def __init__(self, text='', font_size=14, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        font = QFont('Arial', font_size)
        font.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(font)
        self.setText(text)


def setup_ui_remotesvn(self):
    self.event_remotesvn_treeview_render()
    column_widths = [200, 10, 10, 10, 30, 10]
    for _i in range(6):
        self.ui.treeView_remoteSvn.setColumnWidth(_i, column_widths[_i])


def event_remotesvn_connected(self):
    self.ui.label_remotePath.setText("[ROOT] {}".format(self.svn.get_url()))
    self.event_remotesvn_model_refresh()
    self.ui.tabWidget.setCurrentIndex(1)
    self.setup_ui_bundle()


def event_remotesvn_model_refresh(self):
    self.remotesvn_mdl.invisibleRootItem().removeRows(0, self.remotesvn_mdl.rowCount())
    for item in self.svn.list():
        rowlist = func_model_generate_row(item)
        self.remotesvn_mdl.appendRow(rowlist)


def event_remotesvn_treeview_render(self):
    self.ui.label_remotePath.setText("[ROOT] {}".format(self.svn.get_url()))
    self.ui.treeView_remoteSvn.setModel(self.remotesvn_mdl)
    self.ui.treeView_remoteSvn.expandAll()


def event_remotesvn_treeview_menu_list(self):
    indices = self.ui.treeView_remoteSvn.selectedIndexes()
    if len(indices) > 0:
        _index = indices[0]
        pivot = _index.sibling(_index.row(), 0)
        event_remotesvn_treeview_update_subdir(self, pivot)


def event_remotesvn_treeview_menu_mkdir(self):
    pass


def event_remotesvn_treeview_menu_checkout(self):
    pass


def event_remotesvn_treeview_menu_delete(self):
    pass


def event_remotesvn_treeview_menu_rename(self):
    pass


def event_remotesvn_treeview_menu_move(self):
    pass


def event_remotesvn_treeview_menu_find(self):
    pass


def event_remotesvn_treeview_menu_expand(self):
    pass


def event_remotesvn_treeview_menu_refresh(self):
    event_remotesvn_model_refresh(self)


def event_remotesvn_treeview_right_click(self, pos):
    menu = QMenu()
    indices = self.ui.treeView_remoteSvn.selectedIndexes()
    if len(indices) > 0:
        act_list = menu_action('List', self.event_remotesvn_treeview_menu_list)
        act_mkdir = menu_action('MakeDir', self.event_remotesvn_treeview_menu_mkdir)
        act_checkout = menu_action('Checkout', self.event_remotesvn_treeview_menu_checkout)
        act_delete = menu_action('Delete', self.event_remotesvn_treeview_menu_delete)
        act_rename = menu_action('Rename', self.event_remotesvn_treeview_menu_rename)
        act_move = menu_action('MoveTo', self.event_remotesvn_treeview_menu_move)
        act_find = menu_action('Find', self.event_remotesvn_treeview_menu_find)

        menu.addAction(act_list)
        menu.addAction(act_mkdir)
        menu.addAction(act_checkout)
        menu.addAction(act_delete)
        menu.addSeparator()
        menu.addAction(act_rename)
        menu.addAction(act_move)
        menu.addSeparator()
        menu.addAction(act_find)

        submenu_expand = QMenu('Expand')
        act_expand_current = menu_action('Current Dir', self.event_remotesvn_treeview_menu_expand)
        act_expand_recursive = menu_action('Current Dir Recursively', self.event_remotesvn_treeview_menu_expand)
        act_expand_all = menu_action('All Dir', self.event_remotesvn_treeview_menu_expand)
        act_expand_all_recursive = menu_action('All Dir Recursively', self.event_remotesvn_treeview_menu_expand)

        submenu_expand.addAction(act_expand_current)
        submenu_expand.addAction(act_expand_recursive)
        submenu_expand.addAction(act_expand_all)
        submenu_expand.addAction(act_expand_all_recursive)
        menu.addMenu(submenu_expand)

    act_refresh = menu_action('Refresh', self.event_remotesvn_treeview_menu_refresh)
    menu.addSeparator()
    menu.addAction(act_refresh)

    menu.exec_(self.ui.treeView_remoteSvn.viewport().mapToGlobal(pos))


def event_remotesvn_treeview_left_click(self, event):
    _index = self.ui.treeView_remoteSvn.indexAt(event.pos())
    if _index.isValid():
        self.ui.treeView_remoteSvn.setCurrentIndex(_index)
        # pivot = _index.sibling(_index.row(), 0)
        if self.ui.treeView_remoteSvn.isExpanded(_index):
            self.ui.treeView_remoteSvn.collapse(_index)
        else:
            self.ui.treeView_remoteSvn.expand(_index)
    else:
        self.ui.treeView_remoteSvn.clearSelection()


def event_remotesvn_treeview_left_double_click(self, event):
    _index = self.ui.treeView_remoteSvn.indexAt(event.pos())
    if _index.isValid():
        current_index = _index.sibling(_index.row(), 0)
        event_remotesvn_treeview_update_subdir(self, current_index)


def event_remotesvn_treeview_update_subdir(self, current_index):
    if func_model_get_filename(current_index).endswith('/'):
        func_model_clear_row(self.remotesvn_mdl, current_index)
        for item in self.svn.list(func_model_get_fullpath(current_index)):
            func_model_add_row(self.remotesvn_mdl, current_index, item)
        self.ui.treeView_remoteSvn.expand(current_index)
        for _i in range(6):
            self.ui.treeView_remoteSvn.resizeColumnToContents(_i)


def func_model_get_filename(index):
    return index.sibling(index.row(), 0).data()


def func_model_get_fullpath(current_index):
    path = list()
    path.append(func_model_get_filename(current_index))
    ptr = current_index.parent()
    while ptr.data():
        path.append(ptr.data())
        ptr = ptr.parent()

    full_path = ""
    for each in reversed(path):
        full_path += each.replace(" ", "%20").replace("'", "%27").replace('"', "%22")

    return full_path


def func_model_create(parent=None):
    model = QStandardItemModel(0, 6, parent)
    for item in ModelColumn:
        model.setHeaderData(int(item), Qt.Horizontal, item.name)
    return model


def func_model_generate_row(info_list):
    rowlist = [ModelItem(text=info_list[0], font_size=12, set_bold=True)]
    rowlist.extend([ModelItem(text=info_list[i], font_size=12) for i in range(1, len(info_list))])
    return rowlist


def func_model_add_row(model, index, item):
    pivot = index.sibling(index.row(), 0)
    rowlist = func_model_generate_row(item)
    model.itemFromIndex(pivot).appendRow(rowlist)


def func_model_clear_row(model, index):
    item = model.itemFromIndex(index)
    if item.hasChildren():
        item.removeRows(0, item.rowCount())
