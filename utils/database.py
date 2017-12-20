"""------------------------------------------------------------------------------------------------
Program:    database
Py Ver:     2.7
Purpose:    This class module is a lightweight wrapper to help make database connection and
            interfacing easier.

Developer:  J. Berendt
Email:      support@73rdstreetdevelopment.co.uk

Comments:

Use:        >>> import utils.database as db
            >>> ora = db.Oracle(host='my_host', user='my_user', passowrd='my_pass')
            >>> ora.connect()
            >>> ora.connected
            >>> True

---------------------------------------------------------------------------------------------------
UPDATE LOG:
Date        Programmer      Version     Update
20.12.17    J. Berendt      0.1.0       Written  pylint (10/10)
------------------------------------------------------------------------------------------------"""

import utils
import user_interface as ui

# ALLOW ANY NUMBER OF PUBLIC METHODS
# pylint: disable=too-few-public-methods
# ALLOW ANY NUMBER OF INSTANCE ATTRIBUTES
# pylint: disable=too-many-instance-attributes

# ----------------------------------------------------------------------
class Database(object):

    """
    PURPOSE:
    The Database super-class is used to hold general properties or
    functions used by the more specific sub-classes.
    """

    def __init__(self):

        # INITIALISE
        self.conn       = None
        self.cur        = None
        self.connected  = False
        self._ui        = ui.UserInterface()

    # ------------------------------------------------------------------
    def disconnect(self):

        """
        SUMMARY:
        A simple method to close the database connection, and change
        the .connected property to False.
        """

        # CLOSE THE DATABASE CONNECTION
        self.conn.close()
        self.connected = False


    # ------------------------------------------------------------------
    @staticmethod
    def _parse_script(script_string):

        r"""
        PUROSE:
        Helper function used to parse a SQL script file into individual
        statements.

        The parsed statements are returned as a list.

        DESIGN:
        The design is very simple in that a list of statements is
        created and returned using a split() function on the ';'
        character.

        Additionally, parsed statements containing *only* the newline
        character (\n) are removed.  Also, the newline character is
        removed from a line starting with the newline character.

        PARAMETERS:
        - script_string
        The string value of the script to be parsed.
        """

        # PARSE THE SCRIPT INTO INDIVIDUAL STATEMENTS
        cmds = [line for line in script_string.split(';')]

        # LOOP THROUGH EACH STATEMENT
        for idx, cmd in enumerate(cmds):
            # TEST FOR NEWLINE CHAR LINES >> REMOVE THEM
            if cmd == '\n':
                cmds.pop(idx)
            # TEST FOR STATEMENTS STARTWITH WITH A NEWLINE CHARACTER
            elif cmd.startswith('\n'):
                # SLICE TO REMOVE THE STARTING NEWLINE CHARACTER
                cmds[idx] = cmd[1:]

        # RETURN THE CLEANED LIST OF STATEMENTS
        return cmds


    # ------------------------------------------------------------------
    def _table_exists(self, sql):

        """
        SUMMARY:
        This general function tests if a table exists.  The result is
        returned as a boolean value.
        """

        try:
            # RUN QUERY >> CONVERT RESULT TO BOOLEAN
            return bool(self.cur.execute(sql).fetchall()[0][0])

        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_error(err)


# ----------------------------------------------------------------------
class Oracle(Database):

    """
    PURPOSE:
    This class is a lightweight wrapper for cx_Oracle, where commonly
    used cx_Oracle methods and functions have been added as class
    properties.

    PARAMETERS:
    - host
    Database host; or database name
    - user
    Login: user name
    - password
    Login: password
    - from_file (default=False)
    Load the database credentials from a config file
      - valid keys: host, user, password
    - filename
    Full path to the file holding the database credentials

    USE:
    > from utils.database import Oracle
    >
    > # LOAD CREDENTIALS
    > ora = Oracle(host='my_host', user='my_user', password='my_pass')
    >
    > # CONNECT TO THE DB
    > ora.connect()
    > # CHECK CONNECTION WAS SUCCESSFUL
    > ora.connected
    > True
    """

    # ------------------------------------------------------------------
    def __init__(self, host=None, user=None, password=None,
                 from_file=False, filename=None):

        # INHERIT SUPER-CLASS PROPERTIES
        super(Oracle, self).__init__()
        # INITIALISE
        self.connstr    = ''
        self._host      = host
        self._user      = user
        self._password  = password
        self._from_file = from_file
        self._filename  = filename


    # ------------------------------------------------------------------
    def connect(self):

        """
        PURPOSE:
        Method used to update the class' database connection properties.
        The .connected property is a boolean value which can be used
        by the caller to test if the connection was successful.

        DESIGN:
        Function designed to create a connection to an Oracle
        database using the provided login parameters, or directly from
        a config file. If a login detail is not provided, the user is
        prompted; which can be used as a security feature.

        NOTE: To prompt for login details, leave the parameter(s)
        blank.

        Working in the background for the credential validation and
        handling the actual database connection, are several other
        functions which can be found in the utils module.
        """

        try:
            # INITIALISE
            creds = dict()
            dbtype = 'oracle'

            # TEST IF A CONFIG FILE IS TO BE USED
            if self._from_file:
                # DEFINE CREDENTIAL KEYS
                db_keys = ['host', 'user', 'password']
                # GET CREDENTIALS FROM THE CONFIG FILE
                creds = utils._dbconn_fields(dbtype=dbtype, fields=db_keys,
                                             filename=self._filename)
            else:
                # GET CREDENTIALS FROM PASSED PARAMETERS
                creds = utils._dbconn_params(dbtype=dbtype, host=self._host, user=self._user,
                                             password=self._password)

            # TEST IF CREDENTIALS ARE POPULATED
            if creds is not None:
                # CONNECT TO THE DATABASE >> UPDATE CLASS PROPERTIES
                self._connect(creds=creds)

        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_alert('\nAn error occurred while connecting to the Oracle database.')
            self._ui.print_error(err)


    # ------------------------------------------------------------------
    def execute_script(self, sql_file, commit=False):

        """
        PURPOSE:
        This method is designed specifically to handle a full Oracle
        SQL script consisting of multiple SQL statements, as cx_Oracle
        cannot natively handle this.

        DESIGN:
        This method is a wrapper around cx_Oracle's execute() method,
        and accepts the file path for the script to be executed.

        Once the script is parsed into individual statements using
        the ';' character, each individual statement is run using
        cx_Oracle's execute() method.

        PARAMETERS:
        - sql_file
        The full file path to the script to be run.
        - commit (default=False)
        Boolean flag to execute a commit.
        """

        try:
            # INITIALISE
            success = False

            # TEST IF THE FILE EXISTS
            if utils.fileexists(sql_file):
                # RE-INITIALISE (SO FIRST EXECUTE WILL RUN)
                success = True
                # PARSE THE SCRIPT INTO INDIVIDUAL COMMANDS
                cmds = self._parse_script(script_string=open(sql_file).read())

                # LOOP THROUGH EACH STATEMENT
                for cmd in cmds:
                    # EXECUTE COMMAND
                    if success: success = self._execute_commit(sql=cmd, commit=commit)

        except Exception as err:
            success = False
            self._ui.print_error(err)

        return success


    # ------------------------------------------------------------------
    def table_exists(self, table_name):

        """
        SUMMARY:
        This Oracle specific function tests if a table exists, and
        returns a boolean value.

        DESIGN:
        This function wraps the general _table_exists() function and
        provides the SQL statement to be run.

        PARAMETERS:
        - table_name
        The name of the table to be tested
        """

        # BUILD THE SQL STATEMENT
        sql = """
        SELECT count(*) FROM dual WHERE EXISTS (
            SELECT *
            FROM sys.user_tables
            WHERE table_name = '%s'
        )
        """ % table_name.upper()

        # GET >> RETURN BOOLEAN RESULT
        return self._table_exists(sql=sql)


    # ------------------------------------------------------------------
    def _execute_commit(self, sql, commit):

        """
        SUMMARY:
        Simple execute / commit wrapper around cx_Oracle's execute()
        method.
        """

        try:
            # EXECUTE COMMAND
            self.cur.execute(sql)
            # COMMIT?
            if commit: self.conn.commit()
            success = True
        except Exception as err:
            success = False
            self._ui.print_error(err)

        return success


    # ------------------------------------------------------------------
    def _connect(self, creds):

        """
        SUMMARY:
        Private method used to connnect to the database and set the
        class properties.
        """

        try:
            # MAKE THE CONNECTION
            dbo = utils._dbconn_oracle_conn(creds=creds)
            # SET CLASS PROPERTIES
            self.conn       = dbo['conn']
            self.cur        = dbo['cur']
            self.connstr    = '%s/%s@%s' % (creds['user'], creds['password'], creds['host'])
            self.connected  = True
        except Exception:
            self.connected = False


# ----------------------------------------------------------------------
class SQLServer(Database):

    """
    PURPOSE:
    This class is a lightweight wrapper for pyodbc, and used to handle
    database objects for SQL Server.

    PARAMETERS:
    - server
    Name of the server where the SQL Server database lives
    - database
    The name of the database to be connected
    - user
    Login: user name
    - password
    Login: password
    - from_file (default=False)
    Load the database credentials from a config file
      - valid keys: server, database, user, password
    - filename
    Full path to the file holding the database credentials

    USE:
    > from utils.database import SQLServer
    >
    > # LOAD CREDENTIALS
    > sql = SQLServer(server='my_server', database='my_db',
                      user='my_user', password='my_pass')
    >
    > # CONNECT TO THE DB
    > sql.connect()
    > # CHECK CONNECTION WAS SUCCESSFUL
    > sql.connected
    > True
    """

    # ------------------------------------------------------------------
    def __init__(self, server=None, database=None, user=None,
                 password=None, from_file=False, filename=None):

        # INHERIT SUPER-CLASS PROPERTIES
        super(SQLServer, self).__init__()
        # INITIALISE
        self._server    = server
        self._database  = database
        self._user      = user
        self._password  = password
        self._from_file = from_file
        self._filename  = filename


    # ------------------------------------------------------------------
    def connect(self):

        """
        PURPOSE:
        Method used to update the class' database connection properties.
        The .connected property is a boolean value which can be used
        by the caller to test if the connection was successful.

        DESIGN:
        Function designed to create a connection to a SQL Server
        database using the provided login parameters, or directly from
        a config file. If a login detail is not provided, the user is
        prompted; which can be used as a security feature.

        NOTE: To prompt for login details, leave the parameter(s)
        blank.

        Working in the background for the credential validation and
        handling the actual database connection, are several other
        functions which can be found in the utils module.
        """

        try:
            # INITIALISE
            creds = dict()
            dbtype = 'sql_server'

            # TEST IF A CONFIG FILE IS TO BE USED
            if self._from_file:
                # DEFINE CREDENTIAL KEYS
                db_keys = ['server', 'database', 'user', 'password']
                # GET CREDENTIALS FROM THE CONFIG FILE
                creds = utils._dbconn_fields(dbtype=dbtype, fields=db_keys,
                                             filename=self._filename)
            else:
                # GET CREDENTIALS FROM PASSED PARAMETERS
                creds = utils._dbconn_params(dbtype=dbtype, server=self._server,
                                             database=self._database, user=self._user,
                                             password=self._password)

            # TEST IF CREDENTIALS ARE POPULATED
            if creds is not None:
                # CONNECT TO THE DATABASE >> UPDATE CLASS PROPERTIES
                self._connect(creds=creds)

        except Exception as err:
            # USER NOTIFICATION
            self._ui.print_alert('\nAn error occurred while connecting to the SQLServer database.')
            self._ui.print_error(err)


    # ------------------------------------------------------------------
    def table_exists(self, table_name):

        """
        SUMMARY:
        This SQL Server specific function tests if a table exists, and
        returns a boolean value.

        DESIGN:
        This function wraps the general _table_exists() function and
        provides the SQL statement to be run.

        PARAMETERS:
        - table_name
        The name of the table to be tested
        """

        # BUILD SQL STATEMENT
        sql = """
        SELECT count(*)
        FROM INFORMATION_SCHEMA.TABLES
        WHERE table_name = '%s'
        """ % table_name.upper()

        # GET >> RETURN BOOLEAN RESULT
        return self._table_exists(sql=sql)


    # ------------------------------------------------------------------
    def _connect(self, creds):

        """
        SUMMARY:
        Private method used to connnect to the database and set the
        class properties.
        """

        try:
            # MAKE THE CONNECTION
            dbo = utils._dbconn_sql_conn(creds=creds)
            # SET CLASS PROPERTIES
            self.conn       = dbo['conn']
            self.cur        = dbo['cur']
            self.connected  = True
        except Exception:
            self.connected = False
