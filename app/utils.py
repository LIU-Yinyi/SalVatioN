from PyQt5.QtWidgets import QAction


def menu_action(txt, func, tip=None):
    action = QAction(txt)
    action.triggered.connect(func)
    if tip:
        action.setStatusTip(tip)
    return action
