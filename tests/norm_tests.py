import unittest
from copy import copy
from nose.tools import *
from norm.norm import Database, Table, SqliteEngine, MysqlEngine


class SqliteTests(unittest.TestCase):
    def setUp(self):
        self.conn = {'driver': 'sqlite', 'db': 'db.db'}
        self.db = Database(**self.conn)

    def test_withdb(self):
        assert isinstance(self.db, Database)
        assert isinstance(self.db.engine, SqliteEngine)


    def test_select(self):
        dbobj = self.db.select()
        parts = copy(dbobj._parts)
        sqlstring = dbobj.sql()

        listform = [("SELECT", "*")]
        stringform = "SELECT *"

        assert parts == listform
        assert sqlstring == stringform

    def test_from(self):
        dbobj = self.db.from_('mytable')
        parts = copy(dbobj._parts)
        sqlstring = dbobj.sql()

        listform = [("FROM", "mytable")]
        stringform = "FROM mytable"

        assert parts == listform
        assert sqlstring == stringform

    def test_selectfrom(self):
        dbobj = self.db.select().from_('mytable')
        parts = copy(dbobj._parts)
        sqlstring = dbobj.sql()

        listform = [("SELECT", "*"), ("FROM", "mytable")]
        stringform = "SELECT * FROM mytable"

        assert parts == listform
        assert sqlstring == stringform


class MysqlTests(unittest.TestCase):
    def setUp(self):
        self.conn = {'driver': 'mysql', 'db': 'mydb', 'user': 'myuser', \
                'passwd': 'mypass', 'host': 'localhost'}
        self.db = Database(**self.conn)

    def test_withdb(self):
        assert isinstance(self.db, Database)
        assert isinstance(self.db.engine, MysqlEngine)

    def test_select(self):
        dbobj = self.db.select()
        parts = copy(dbobj._parts)
        sqlstring = dbobj.sql()

        listform = [('SELECT', '*')]
        stringform = "SELECT *"

        assert parts == listform
        assert sqlstring == stringform

    def test_selectmultiplecolumns(self):
        dbobj = self.db.select("name", "org")

        parts = copy(dbobj._parts)
        sqlstring = dbobj.sql()

        listform = [("SELECT", "name", "org")]
        stringform = "SELECT `name`, `org`"

        assert parts == listform
        assert sqlstring == stringform

