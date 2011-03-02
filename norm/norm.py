class Engine(object):
    commands = dict(
        SELECT = "SELECT {0}",
        FROM = "FROM {0}",
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

    def __init__(self):
        pass

    def connect(self, *args, **kwargs):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def buildsql(self):
        raise NotImplementedError



class Database(object):
    def __init__(self, *args, **kwargs):
        pass


    def __enter__(self):
        return self
    def __exit__(self, type_, value, traceback):
        return False


    def connect(self):
        pass
    def disconnect(self):
        pass


    def createtable(self, table):
        pass
    def droptable(self, table):
        pass


    def table(self, table):
        return Table(self, table)




class Table(object):
    def __init__(self, db, table):
        pass

    def __enter__(self):
        return self
    def __exit__(self, type_, value, traceback):
        return False


    def select(self, *args, **kwargs):
        pass

    def where(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass
