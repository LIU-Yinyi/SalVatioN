import os
import re
import pexpect
from lxml import etree
from pathlib import Path


class Client:
    def __init__(self, **kwargs):
        self._env = os.environ.copy()
        self._address = kwargs.get("address", "")
        self._username = kwargs.get("username", "")
        self._password = kwargs.get("password", "")
        self._sshkey = kwargs.get("sshkey", "")
        self._url = kwargs.get("url", "")
        self._timeout = kwargs.get("timeout", 10)

        if self._url == "" and self._address != "" and self._username != "":
            self._url = "svn+ssh://{}@{}".format(self._username, self._address.rstrip("/"))

    def get_config(self):
        return {"username": self._username,
                "password": self._password,
                "sshkey": self._sshkey,
                "address": self._address}

    def get_url(self):
        if self._url == "" and self._address != "" and self._username != "":
            self._url = "svn+ssh://{}@{}".format(self._username, self._address.rstrip("/"))
        return self._url

    @staticmethod
    def _run_command(*args):
        cmd = ""
        for arg in args:
            cmd += arg + " "
        res = pexpect.run(cmd.strip())
        return res

    def login(self, **kwargs):
        _remain = kwargs.get("remain", True) # remain initialization config
        self._address = kwargs.get("address", self._address if _remain else "")
        self._username = kwargs.get("username", self._username if _remain else "")
        self._password = kwargs.get("password", self._password if _remain else "")
        self._sshkey = kwargs.get("sshkey", self._sshkey if _remain else "")
        self._url = kwargs.get("url", self._url if _remain else "")
        self.get_url()

        # print(self.get_config())
        flag = False

        if self._sshkey != "":
            _proc = pexpect.spawn('svn', ['list', '--xml', self.get_url()])
            _index = _proc.expect(['<entry', 'svn: E170013: Unable to connect to a repository at URL',
                                   pexpect.EOF, pexpect.TIMEOUT], timeout=self._timeout)
            # print(_proc.before)
            if _index == 0:
                flag = True
                print('have sshkey')
            elif _index == 1:
                print('sshkey error')
        elif self._password != "":
            _proc = pexpect.spawn('svn', ['list', '--xml', self.get_url()])
            _index = _proc.expect(['<entry', 'password', pexpect.EOF, pexpect.TIMEOUT], timeout=self._timeout)
            # print(_proc.before)
            if _index == 0:
                flag = True
                print('have sshkey')
            elif _index == 1:
                _proc.sendline(self._password)
                _subindex = _proc.expect(['<entry', 'svn: E170013: Unable to connect to a repository at URL',
                                          pexpect.EOF, pexpect.TIMEOUT], timeout=self._timeout)
                if _subindex == 0:
                    flag = True
                    print('ok')
                elif _subindex == 1:
                    print('password wrong')
                else:
                    print('other error')
            elif _index == 2:
                print('error')
            elif _index == 3:
                print('timeout')
            _proc.close()
        return flag

    def list(self, rel_path=""):
        path = self.get_url() + '/' + rel_path
        res = list()
        if self._sshkey != "":
            _xml = self._run_command('svn ls --xml', path).strip()
        elif self._password != "":
            _proc = pexpect.spawn('svn', ['list', '--xml', path])
            _index = _proc.expect(['password', pexpect.EOF, pexpect.TIMEOUT], timeout=self._timeout)
            if _index == 0:
                _proc.sendline(self._password)
                _subindex = _proc.expect(['</lists>', pexpect.EOF, pexpect.TIMEOUT], timeout=self._timeout)
                if _subindex == 0:
                    _xml = '<list>' + _proc.before.decode('utf-8').lstrip(':').strip()
                else:
                    return []
            else:
                return []
        else:
            return []

        try:
            _par = etree.XML(_xml)
            for entry in _par.iter('entry'):
                vlist = list()
                if entry.get('kind') == 'file':
                    vlist.append(entry.xpath('string(name)'))
                    _size = int(entry.xpath('string(size)'))
                    _level = 0
                    _units = ["B", "KB", "MB", "GB", "TB"]
                    while _size > 1024 and _level < len(_units) - 1:
                        _size /= 1024.0
                        _level += 1
                    if _level == 0:
                        vlist.append("{:d}{}".format(_size, _units[_level]))
                    else:
                        vlist.append("{:.2f}{}".format(_size, _units[_level]))
                elif entry.get('kind') == 'dir':
                    vlist.append(entry.xpath('string(name)') + '/')
                    vlist.append('--')
                vlist.append('remote')
                vlist.append(entry.xpath('string(commit/@revision)'))
                vlist.append(entry.xpath('string(commit/author)').split('@')[0])
                _date_time = entry.xpath('string(commit/date)')
                vlist.append('{} {}'.format(_date_time[:10], _date_time[11:19]))
                res.append(vlist)
        except Exception as ex:
            print('[Warn] unexpected xml format.')
            print(ex)
        return res

    def mkdir(self, rel_path):
        path = self.get_url() + '/' + rel_path
        return self._run_command('svn mkdir', path)

    def checkout(self, rel_path, save_path):
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        path = self.get_url() + '/' + rel_path
        if self._sshkey != "":
            _ret = self._run_command('svn checkout {} {}'.format(path, save_path))
        elif self._password != "":
            _proc = pexpect.spawn('svn', ['checkout', path, save_path])
            _index = _proc.expect(["password", pexpect.EOF, pexpect.TIMEOUT], timeout=self._timeout)
            if _index == 0:
                _proc.sendline(self._password)
                _ret = _proc.before
            else:
                _ret = None
        else:
            _ret = None
        return _ret
