import os
import sqlite3


def load_bundle():
    if not os.path.exists('cfg/bundle.db'):
        con = sqlite3.connect('cfg/bundle.db')
        cur = con.cursor()
        cur.execute("create table repos (id INTEGER PRIMARY KEY AUTOINCREMENT, alias TEXT, username TEXT, "
                    "password TEXT, sshkey TEXT, address TEXT, autocfg INTEGER);")
        con.commit()
        con.close()
    con = sqlite3.connect('cfg/bundle.db')
    cur = con.cursor()
    cur.execute("select id, alias, username, password, sshkey, address, autocfg from repos;")
    tmp = cur.fetchall()
    con.close()
    return tmp


def save_bundle(cfg_dict):
    if not all(k in cfg_dict for k in ("username", "password", "sshkey", "address", "alias", "autocfg")):
        return False
    if cfg_dict['username'] == "" or cfg_dict['address'] == "":
        return False

    con = sqlite3.connect('cfg/bundle.db')
    cur = con.cursor()
    cur.execute("select id, alias, username, password, sshkey, address, autocfg from repos;")
    res = cur.fetchall()

    is_exist_flag = False
    for item in res:
        if cfg_dict['username'] == item[2] and cfg_dict['address'] == item[5]:
            is_exist_flag = True
            cur.execute("update repos set alias = '{}', password = '{}', sshkey = '{}', autocfg = {} "
                        "where id = {};".format(cfg_dict['alias'], cfg_dict['password'],
                                                cfg_dict['sshkey'], int(cfg_dict['autocfg']), item[0]))
            break

    if is_exist_flag:
        pass
    else:
        cur.execute("insert into repos (alias, username, password, sshkey, address, autocfg) values ('{}', '{}', '{}',"
                    " '{}', '{}', '{}');".format(cfg_dict['alias'], cfg_dict['username'], cfg_dict['password'],
                                                 cfg_dict['sshkey'], cfg_dict['address'], int(cfg_dict['autocfg'])))
    con.commit()
    con.close()
    return True


def delete_bundle(**kwargs):
    _id = kwargs.get("id", -1)
    _username = kwargs.get("username", None)
    _address = kwargs.get("address", None)

    if _id < 0 and (_username is None and _address is None):
        return False

    con = sqlite3.connect('cfg/bundle.db')
    cur = con.cursor()
    cmd = "delete from repos where "
    if _id >= 0:
        cmd += "id = {} and ".format(_id)
    if _username:
        cmd += "username = '{}' and ".format(_username)
    if _address:
        cmd += "address = '{}'".format(_address)

    cur.execute(cmd.rstrip(" and ") + ";")
    con.commit()
    con.close()
    return True
