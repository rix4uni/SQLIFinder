import re
import sys
import argparse
import urllib.parse
import requests
import concurrent.futures
import random
import regex

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--threads", "-t", type=int, default=8, help="number of threads to use")
args = parser.parse_args()

payloads = ["'", '"', '+', '-', '*', '[]', "')"]

# Read the input URLs from sys.stdin
url_list = sys.stdin.read().splitlines()


def check_url(url, payload):
    # Use a regular expression to replace all values in the query string with the payload
    cleaned_url = re.sub(r'=([^&]*)', f'={urllib.parse.quote(payload)}', url)
    decoded_url = urllib.parse.unquote(cleaned_url)

    # Send a request
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3 Edge/16.16299",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    ]

    headers = {"User-Agent": random.choice(user_agents)}

    response = requests.get(decoded_url, headers=headers)

    # Use the | character to search for multiple regular expressions
    MySQL_regex = "Warning.*?\\Wmysqli?_|SQL syntax.*?MySQL|MySQLSyntaxErrorException|SQL syntax.*?MySQL|Warning.*?\\Wmysqli?_|MySQLSyntaxErrorException|valid MySQL result|check the manual that (corresponds to|fits) your MySQL server version|Unknown column '[^ ]+' in 'field list'|MySqlClient\\.|com\\.mysql\\.jdbc|Zend_Db_(Adapter|Statement)_Mysqli_Exception|Pdo[./_\\\\]Mysql|MySqlException|SQLSTATE\\[\\d+\\]: Syntax error or access violation"
    MariaDB_regex = "check the manual that (corresponds to|fits) your MariaDB server version"
    Drizzle_regex = "check the manual that (corresponds to|fits) your Drizzle server version"
    MemSQL_regex = "MemSQL does not support this type of query|is not supported by MemSQL|unsupported nested scalar subselect"
    PostgreSQL_regex = "PostgreSQL.*?ERROR|Warning.*?\\Wpg_|valid PostgreSQL result|Npgsql\\.|PG::SyntaxError:|org\\.postgresql\\.util\\.PSQLException|ERROR:\\s\\ssyntax error at or near|ERROR: parser: parse error at or near|PostgreSQL query failed|org\\.postgresql\\.jdbc|Pdo[./_\\\\]Pgsql|PSQLException"
    Microsoft_SQL_Server_regex = "Driver.*? SQL[\\-\\_\\ ]*Server|OLE DB.*? SQL Server|\\bSQL Server[^&lt;&quot;]+Driver|Warning.*?\\W(mssql|sqlsrv)_|\\bSQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}|System\\.Data\\.SqlClient\\.SqlException\\.(SqlException|SqlConnection\\.OnError)|(?s)Exception.*?\\bRoadhouse\\.Cms\\.|Microsoft SQL Native Client error '[0-9a-fA-F]{8}|\\[SQL Server\\]|ODBC SQL Server Driver|ODBC Driver \\d+ for SQL Server|SQLServer JDBC Driver|com\\.jnetdirect\\.jsql|macromedia\\.jdbc\\.sqlserver|Zend_Db_(Adapter|Statement)_Sqlsrv_Exception|com\\.microsoft\\.sqlserver\\.jdbc|Pdo[./_\\\\](Mssql|SqlSrv)|SQL(Srv|Server)Exception|Unclosed quotation mark after the character string"
    Microsoft_Access_regex = "Microsoft Access (\\d+ )?Driver|JET Database Engine|Access Database Engine|ODBC Microsoft Access|Syntax error \\(missing operator\\) in query expression"
    Oracle_regex = "\\bORA-\\d{5}|Oracle error|Oracle.*?Driver|Warning.*?\\W(oci|ora)_|quoted string not properly terminated|SQL command not properly ended|macromedia\\.jdbc\\.oracle|oracle\\.jdbc|Zend_Db_(Adapter|Statement)_Oracle_Exception|Pdo[./_\\\\](Oracle|OCI)|OracleException"
    IBM_DB2_regex = "CLI Driver.*?DB2|DB2 SQL error|\\bdb2_\\w+\\(|SQLCODE[=:\\d, -]+SQLSTATE|com\\.ibm\\.db2\\.jcc|Zend_Db_(Adapter|Statement)_Db2_Exception|Pdo[./_\\\\]Ibm|DB2Exception|ibm_db_dbi\\.ProgrammingError"
    Informix_regex = "Warning.*?\\Wifx_|Exception.*?Informix|Informix ODBC Driver|ODBC Informix driver|com\\.informix\\.jdbc|weblogic\\.jdbc\\.informix|Pdo[./_\\\\]Informix|IfxException"
    Firebird_regex = "Dynamic SQL Error|Warning.*?\\Wibase_|org\\.firebirdsql\\.jdbc|Pdo[./_\\\\]Firebird"
    SQLite_regex = "SQLite/JDBCDriver|SQLite\\.Exception|(Microsoft|System)\\.Data\\.SQLite\\.SQLiteException|Warning.*?\\W(sqlite_|SQLite3::)|\\[SQLITE_ERROR\\]|SQLite error \\d+:|sqlite3.OperationalError:|SQLite3::SQLException|org\\.sqlite\\.JDBC|Pdo[./_\\\\]Sqlite|SQLiteException"
    SAP_MaxDB_regex = "SQL error.*?POS([0-9]+)|Warning.*?\\Wmaxdb_|DriverSapDB|-3014.*?Invalid end of SQL statement|com\\.sap\\.dbtech\\.jdbc|\\[-3008\\].*?: Invalid keyword or missing delimiter"
    Sybase_regex = "Warning.*?\\Wsybase_|Sybase message|Sybase.*?Server message|SybSQLException|Sybase\\.Data\\.AseClient|com\\.sybase\\.jdbc"
    Ingres_regex = "Warning.*?\\Wingres_|Ingres SQLSTATE|Ingres\\W.*?Driver|com\\.ingres\\.gcf\\.jdbc"
    FrontBase_regex = "Exception (condition )?\\d+\\. Transaction rollback|com\\.frontbase\\.jdbc|Syntax error 1. Missing|(Semantic|Syntax) error [1-4]\\d{2}\\."
    HSQLDB_regex = "Unexpected end of command in statement \\[|Unexpected token.*?in statement \\[|org\\.hsqldb\\.jdbc"
    H2_regex = "org\\.h2\\.jdbc|\\[42000-192\\]"
    MonetDB_regex = "![0-9]{5}![^\\n]+(failed|unexpected|error|syntax|expected|violation|exception)|\\[MonetDB\\]\\[ODBC Driver|nl\\.cwi\\.monetdb\\.jdbc"
    Apache_Derby_regex = "Syntax error: Encountered|org\\.apache\\.derby|ERROR 42X01"
    Vertica_regex = ", Sqlstate: (3F|42).{3}, (Routine|Hint|Position):|/vertica/Parser/scan|com\\.vertica\\.jdbc|org\\.jkiss\\.dbeaver\\.ext\\.vertica|com\\.vertica\\.dsi\\.dataengine"
    Mckoi_regex = "com\\.mckoi\\.JDBCDriver|com\\.mckoi\\.database\\.jdbc|&lt;REGEX_LITERAL&gt;"
    Presto_regex = "com\\.facebook\\.presto\\.jdbc|io\\.prestosql\\.jdbc|com\\.simba\\.presto\\.jdbc|UNION query has different number of fields: \\d+, \\d+"
    Altibase_regex = "Altibase\\.jdbc\\.driver"
    MimerSQL_regex = "com\\.mimer\\.jdbc|Syntax error,[^\\n]+assumed to mean"
    CrateDB_regex = "io\\.crate\\.client\\.jdbc"
    Cache_regex = "encountered after end of query|A comparison operator is required here"
    Raima_Database_Manager_regex = "-10048: Syntax error|rdmStmtPrepare\\(.+?\\) returned"
    Virtuoso_regex = "SQ074: Line \\d+:|SR185: Undefined procedure|SQ200: No table |Virtuoso S0002 Error|\\[(Virtuoso Driver|Virtuoso iODBC Driver)\\]\\[Virtuoso Server\\]"

    # Find all matches for the regular expressions
    mysql_matches = regex.finditer(MySQL_regex, response.text)
    mariadb_matches = regex.finditer(MariaDB_regex, response.text)
    drizzle_matches = regex.finditer(Drizzle_regex, response.text)
    memsql_matches = regex.finditer(MemSQL_regex, response.text)
    postgresql_matches = regex.finditer(PostgreSQL_regex, response.text)
    microsoft_sql_server_matches = regex.finditer(Microsoft_SQL_Server_regex, response.text)
    microsoft_access_matches = regex.finditer(Microsoft_Access_regex, response.text)
    oracle_matches = regex.finditer(Oracle_regex, response.text)
    ibm_db2_matches = regex.finditer(IBM_DB2_regex, response.text)
    informix_matches = regex.finditer(Informix_regex, response.text)
    firebird_matches = regex.finditer(Firebird_regex, response.text)
    sqlite_matches = regex.finditer(SQLite_regex, response.text)
    sap_maxdb_matches = regex.finditer(SAP_MaxDB_regex, response.text)
    sybase_matches = regex.finditer(Sybase_regex, response.text)
    ingres_matches = regex.finditer(Ingres_regex, response.text)
    frontbase_matches = regex.finditer(FrontBase_regex, response.text)
    hsqldb_matches = regex.finditer(HSQLDB_regex, response.text)
    h2_matches = regex.finditer(H2_regex, response.text)
    monetdb_matches = regex.finditer(MonetDB_regex, response.text)
    apache_derby_matches = regex.finditer(Apache_Derby_regex, response.text)
    vertica_matches = regex.finditer(Vertica_regex, response.text)
    mckoi_matches = regex.finditer(Mckoi_regex, response.text)
    presto_matches = regex.finditer(Presto_regex, response.text)
    altibase_matches = regex.finditer(Altibase_regex, response.text)
    mimersql_matches = regex.finditer(MimerSQL_regex, response.text)
    cratedb_matches = regex.finditer(CrateDB_regex, response.text)
    cache_matches = regex.finditer(Cache_regex, response.text)
    raima_database_manager_matches = regex.finditer(Raima_Database_Manager_regex, response.text)
    virtuoso_matches = regex.finditer(Virtuoso_regex, response.text)

    # Print out any matches that were found
    for mysql_match in mysql_matches:
        print(f"\033[1;31mVULNERABLE [MySQL]: {decoded_url}\033[0;0m")

    for mariadb_match in mariadb_matches:
        print(f"\033[1;31mVULNERABLE [MariaDB]: {decoded_url}\033[0;0m")

    for drizzle_match in drizzle_matches:
        print(f"\033[1;31mVULNERABLE [Drizzle]: {decoded_url}\033[0;0m")

    for memsql_match in memsql_matches:
        print(f"\033[1;31mVULNERABLE [MemSQL]: {decoded_url}\033[0;0m")

    for postgresql_match in postgresql_matches:
        print(f"\033[1;31mVULNERABLE [PostgreSQL]: {decoded_url}\033[0;0m")

    for microsoft_sql_server_match in microsoft_sql_server_matches:
        print(f"\033[1;31mVULNERABLE [Microsoft_SQL_Server]: {decoded_url}\033[0;0m")

    for microsoft_access_match in microsoft_access_matches:
        print(f"\033[1;31mVULNERABLE [Microsoft_Access]: {decoded_url}\033[0;0m")

    for oracle_match in oracle_matches:
        print(f"\033[1;31mVULNERABLE [Oracle]: {decoded_url}\033[0;0m")

    for ibm_db2_match in ibm_db2_matches:
        print(f"\033[1;31mVULNERABLE [IBM_DB2]: {decoded_url}\033[0;0m")

    for informix_match in informix_matches:
        print(f"\033[1;31mVULNERABLE [Informix]: {decoded_url}\033[0;0m")

    for firebird_match in firebird_matches:
        print(f"\033[1;31mVULNERABLE [Firebird]: {decoded_url}\033[0;0m")

    for sqlite_match in sqlite_matches:
        print(f"\033[1;31mVULNERABLE [SQLite]: {decoded_url}\033[0;0m")

    for sap_maxdb_match in sap_maxdb_matches:
        print(f"\033[1;31mVULNERABLE [SAP_MaxDB]: {decoded_url}\033[0;0m")

    for sybase_match in sybase_matches:
        print(f"\033[1;31mVULNERABLE [Sybase]: {decoded_url}\033[0;0m")

    for ingres_match in ingres_matches:
        print(f"\033[1;31mVULNERABLE [Ingres]: {decoded_url}\033[0;0m")

    for frontbase_match in frontbase_matches:
        print(f"\033[1;31mVULNERABLE [FrontBase]: {decoded_url}\033[0;0m")

    for hsqldb_match in hsqldb_matches:
        print(f"\033[1;31mVULNERABLE [HSQLDB]: {decoded_url}\033[0;0m")

    for h2_match in h2_matches:
        print(f"\033[1;31mVULNERABLE [H2]: {decoded_url}\033[0;0m")

    for monetdb_match in monetdb_matches:
        print(f"\033[1;31mVULNERABLE [MonetDB]: {decoded_url}\033[0;0m")

    for apache_derby_match in apache_derby_matches:
        print(f"\033[1;31mVULNERABLE [Apache_Derby]: {decoded_url}\033[0;0m")

    for vertica_match in vertica_matches:
        print(f"\033[1;31mVULNERABLE [Vertica]: {decoded_url}\033[0;0m")

    for mckoi_match in mckoi_matches:
        print(f"\033[1;31mVULNERABLE [Mckoi]: {decoded_url}\033[0;0m")

    for presto_match in presto_matches:
        print(f"\033[1;31mVULNERABLE [Presto]: {decoded_url}\033[0;0m")

    for altibase_match in altibase_matches:
        print(f"\033[1;31mVULNERABLE [Altibase]: {decoded_url}\033[0;0m")

    for mimersql_match in mimersql_matches:
        print(f"\033[1;31mVULNERABLE [MimerSQL]: {decoded_url}\033[0;0m")

    for cratedb_match in cratedb_matches:
        print(f"\033[1;31mVULNERABLE [CrateDB]: {decoded_url}\033[0;0m")

    for cache_match in cache_matches:
        print(f"\033[1;31mVULNERABLE [Cache]: {decoded_url}\033[0;0m")

    for raima_database_manager_match in raima_database_manager_matches:
        print(f"\033[1;31mVULNERABLE [Raima_Database_Manager]: {decoded_url}\033[0;0m")

    for virtuoso_match in virtuoso_matches:
        print(f"\033[1;31mVULNERABLE [Virtuoso]: {decoded_url}\033[0;0m")


# Create a ThreadPoolExecutor with the specified number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
    # Iterate over the payloads
    for payload in payloads:
        # Iterate over the URLs
        for url in url_list:
            try:
                # Submit the task to the executor
                future = executor.submit(check_url, url, payload)
                # Wait for the task to complete
                future.result()
            except KeyboardInterrupt:
                exit(0)
