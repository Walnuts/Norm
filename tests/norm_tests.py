from nose.tools import *
from norm.norm import Database, Table

def setup():
    pass

def teardown():
    pass

@with_setup(setup, teardown)
def test_with_db():
    db = Database()
    with db:
        assert_true( isinstance(db, Database) )

@with_setup(setup, teardown)
def test_with_table():
    db = Database()
    with db.table('testtable') as table:
        assert_true( isinstance(table, Table) )

