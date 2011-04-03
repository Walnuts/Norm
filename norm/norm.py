from itertools import imap

class Engine(object):
    """
    Base class for Sql Engines.  Not to be used by itself, as
    it needs to be subclassed with database-specific connection
    information.  The `commands` dict is also here to be overriden
    in the event of a difference in a specific SQL implementation.
    """

    def __init__(self, *args, **kwds):
        self.commands = dict(
            SELECT = self.__select__,
            FROM = self.__from__,
            INSERT = "INSERT INTO {0} ({1})",
            VALUES = "VALUES ({0})",
            UPDATE = "UPDATE {0}",
            SET = "SET {1}",
            DELETE = "DELETE FROM {0}",
            WHERE = "WHERE {0}",
            ORDERBY = "ORDER BY {0}",
            JOIN = "INNER JOIN {0}",
            ON = "ON {0}={1}",
            GROUPBY = "GROUP BY {0}",
            HAVING = "HAVING {0}",
            CREATETABLE = "CREATE TABLE IF NOT EXISTS {0} ({1})",
            DROPTABLE = "DROP TABLE IF EXISTS {0}"
        )

        self.types = dict(
            pk="{0} INTEGER PRIMARY KEY AUTOINCREMENT",
            string="{0} TEXT {1}",
            integer="{0} INTEGER {1}",
            bool="{0} INTEGER {1}",
            fk="{0} INTEGER {1}",
            references="FOREIGN KEY({0}) REFERENCES {1}({2})"
        )

    def connect(self, *args, **kwds):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def sql(self, parts):
        formatted = []
        for tup in parts:
            k = tup[0]
            v = tup[1:]
            command = self.commands.get(k)
            if isinstance(command, basestring):
                formatted.append(command.format(*v))
            else:
                fmtdstring = command(*v)
                formatted.append(fmtdstring)

        return " ".join(formatted)

    def wrap(self, value):
        raise NotImplementedError

    def __select__(self, *args):
        try:
            args = list(imap(self.wrap, args))
        except NotImplementedError:
            args = list(args)
        fmtd = ", ".join(args)
        final = "SELECT {0}".format(fmtd)
        return final

    def __from__(self, *args):
        fmtd = ", ".join(list(args))
        final = "FROM {0}".format(fmtd)
        return final


class SqliteEngine(Engine):
    def __init__(self, **kwds):
        import sqlite3
        self.db = kwds.pop('db')
        assert self.db is not None
        super(SqliteEngine, self).__init__(**kwds)


    def connect(self, **kwds):
        pass


class MysqlEngine(Engine):
    def __init__(self, **kwds):
        self.user = kwds.pop('user')
        self.passwd = kwds.pop('passwd')
        self.host = kwds.pop('host')
        self.db = kwds.pop('db')
        super(MysqlEngine, self).__init__(**kwds)

    def wrap(self, value):
        if value != "*":
            return "`{0}`".format(value)
        return value

class PostgresqlEngine(Engine):
    pass
class MssqlEngine(Engine):
    pass
class Db2Engine(Engine):
    pass
class FirebirdEngine(Engine):
    pass


ENGINES = {
        'sqlite': SqliteEngine,
        'mysql': MysqlEngine,
        'postgres': PostgresqlEngine,
        'pgsql': PostgresqlEngine,
        'mssql': MssqlEngine,
        'db2': Db2Engine,
        'firebird': FirebirdEngine
        }

class SqlFragmentError(Exception):
    pass

class SqlParts(list):
    __VALID_PARTS__ = (
            "SELECT",
            "FROM",
            "WHERE",
            "CREATETABLE",
            "DROPTABLE"
            )
    def __init__(self, *args, **kwds):
        super(SqlParts, self).__init__(*args, **kwds)

    def flush(self):
        tmp = list(self)
        list.__delslice__(self, 0, len(self))
        return tmp

    def append(self, obj):
        try:
            assert type(obj) == tuple
        except AssertionError:
            raise TypeError("please pass a tuple")

        try:
            assert obj[0] in self.__VALID_PARTS__
        except AssertionError:
            raise SqlFragmentError("{0} is an invalid key".format(obj[0]))

        list.append(self, obj)




class Database(object):
    def __init__(self, **kwds):
        self._parts = SqlParts()
        self.driver = kwds.pop('driver')
        self.engine = ENGINES[self.driver](**kwds)

        assert self.engine is not None


    def __enter__(self):
        return self
    def __exit__(self, type_, value, traceback):
        return False


    def connect(self):
        pass
    def disconnect(self):
        pass

    def sql(self):
        parts = self._parts.flush()
        return self.engine.sql(parts)


    def createtable(self, table, fields):
        """
        Is just a "dumb" create table function. That is, it doesn't enforce
        any foreign key checks.  If you try to create a table with a foreign
        key to a table that doesn't exist yet, it will not succeed if you
        try to do a .X().

        >>> from norm.fields import *
        >>> from norm import Database
        >>> dbconnect = dict(host='localhost', user='mydbuser',
        ...                 passwd='mypass', db='mydb', driver='mysql')
        >>> fields = (
        ...         String('name'),
        ...         ForeignKey('myothertable'),
        ...         DateTime('created'),
        ...         DateTime('modified')
        ...         )
        >>> 
        >>> with Database(**dbconnect) as db:
        ...     db.createtable('mytable', fields).sql()
        "CREATE TABLE `mytable` (`id` INT PRIMARY KEY AUTO_INCREMENT, `name`
        VARCHAR(255) NOT NULL, `myothertable_id` INT, `created`
        DATETIME, `modified` DATETIME, FOREIGN KEY (`myothertable_id`)
        REFERENCES `myothertable`(`id`)"
        >>> 
        >>> 
        >>> 
        >>> # other syntax:
        >>> fields = ('string::name', 'fk::myothertable', 'datetime::created', \
        ...         'datetime::modified')
        >>> with Database(**dbconnect) as db:
        ...     db.createtable('mytable', fields).sql()
        "CREATE TABLE `mytable` (`id` INT PRIMARY KEY AUTO_INCREMENT, `name`
        VARCHAR(255) NOT NULL, `myothertable_id` INT, `created`
        DATETIME, `modified` DATETIME, FOREIGN KEY (`myothertable_id`)
        REFERENCES `myothertable`(`id`)"
        """
        return self

    def droptable(self, table):
        """
        Is just a "dumb" drop table sql generator. That is, it won't enforce
        any foreign key checks.  If you try to drop a table that another 
        table still defends on, an error will occur.

        >>> from norm import Database
        >>> dbconnect = dict(host='localhost', user='mydbuser',
        ...                 passwd='mypass', db='mydb', driver='mysql')
        >>> with Database(**dbconnect) as db:
        ...     db.droptable('mytable')
        >>> 
        """
        pass

    def select(self, *columns):
        if not columns:
            columns = ("*",)
        args = ("SELECT",) + columns
        self._parts.append(args)
        return self

    def from_(self, *tables):
        assert len(tables) > 0
        args = ("FROM",) + tables
        self._parts.append(args)
        return self

    def where(self, *args, **kwds):
        return self

    def table(self, table):
        return Table(self, table)




"""
My thought is that `Table` will inherit all methods from `Database`, with
the only difference being that using a `Table` objects restricts you to
doing operations on one table at a time, with the benefit being that you
don't have to use the `table()` method like you do when doing queries on
a `Database` object.

e.g., instead of

    >>> with Database('mydb') as db:
    ...     db.select().from('mytable').where('blah = blah')

you would do:

    >>> with Database('mydb').table('mytable') as table:
    ...     table.select().where('blah=blah')
"""
class Table(Database):
    pass

