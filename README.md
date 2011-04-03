# NORM

NORM (_N_ot an _O_bject-_Relational_ _M_apper) is a SQL abstraction
library that sits somewhere between raw queries and full on ORMs in
terms of features.

The goal of NORM is to have the means to abstract away the differences
between SQL DDL and DML implementations, but not necessarily mapping
entities to objects.

I started building this when I would write small projects that I didn't
want to bog down with SQLAlchemy models.  Since I prefer Postgres to
Mysql, I wanted to develop the application locally using pg, which was a
problem when I had to deploy the application and use my organizations
MySQL or MsSql servers.

There are 2 ways of using NORM.  The most basic way is to use it _just_
above the DBApi to allow the programmer to switch database engines
without having to rewrite queries to accomodate the slight differences
in SQL implementations. Below is an example of using NORM for SQL
abstraction:

    >>> db = Database(driver='mysql', **connection_params)
    >>> db.select('name', 'organization').from_('users').where(('position__like', '%manager%')).sql()
    "SELECT `name`, `organization` FROM `users` WHERE `position` LIKE '%manager%'"
    >>>
    >>> db = Database(driver='postgresql', **connection_params)
    >>> db.select('name', 'organization').from_('users').where(('position__like', '%manager%')).sql()
    "SELECT name, organization FROM users WHERE position LIKE '%manager%'"

The other way to use it is to use it in place of
a DBApi library to execute queries and retrieve results.  This is not
going to be very full-featured at first, with only a few methods
available.

Here is an example of using NORM in place of a DBApi library:

    >>> with Database(driver='sqlite', db='.db') as db:
    ...     db.select().from_('mytable').x() # .x() is short for .execute()
    {'col1': 'value 1', 'col2': 'value 2', 'id': 1L, ... }

Notice that you can use the `with` statement to ensure that your
database connection is opened and closed properly. Also notice that when
the query results come back, they are in a standard Python dictionary.
So far, that is one of the main restrictions of NORM queries: your
results will be either a dict (if there was only one row returned) or a list
of dicts (if there is more than one row returned). INSERT queries return
the lastrowid, and UPDATE and DELETE queries return the boolean value of
whether the query succeeded or not.

Where NORM really shines is when used for SQL DDL statements, where
oftentimes you will see the most difference between SQL implementations.
This allows the programmer to easily switch database engines, by using a
simple python script with NORM and a few `db.createtable(...)`
statements.

    >>> fields = (
    ...         String('name'),
    ...         ForeignKey('othertable'),
    ...         DateTime('created'),
    ...         DateTime('modified')
    ...         )
    >>>
    >>> # or
    >>>
    >>> fields = (
    ...         "string::name",
    ...         "fk::othertable",
    ...         "datetime::created",
    ...         "datetime::modified"
    ...         )
    >>>
    >>> db = Database(driver='mysql', **connection_params)
    >>> db.createtable('mytable', fields).sql()
    "CREATE TABLE IF NOT EXISTS `mytable` (`id` INT PRIMARY KEY AUTO_INCREMENT, `name` VARCHAR(255) NOT NULL, `othertable_id` INT NOT NULL, `created` DATETIME NOT NULL, `modified` DATETIME NOT NULL, FOREIGN KEY (`othertable_id`) REFERENCES `othertable`(`id`)"

Obviously, this is not right for all situations, as abstracting away
details of the individual SQL implementations can cause loss of some
features of your database engine, especially if one engine offers a
feature that others don't. That's not to say that this brings all
capaibilities down to SQLite's feature level, but hardcore SQL pros will
surely run into situations where NORM just won't support certain use
cases.

