import configparser
import psycopg2

# APIキーやRDSの情報を設定ファイルから読み込む
config = configparser.ConfigParser()
config.read('config/config.ini')
ENDPOINT = config.get('rds', 'endpoint')
PORT = config.get('rds', 'port')
DATABASE = config.get('rds', 'database_name')
USERNAME = config.get('rds', 'username')
PASSWORD = config.get('rds', 'password')
REGION = config.get('rds', 'region')

def saveContractSourceCodeToDB(contract_address, contract_name, file_name, source):
    try:
        # RDSへの接続
        conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
    except Exception:
        print("DB CONNECTION ERROR at saveContractSourceCodeToDB")
        saveContractSourceCodeToDB(contract_address, contract_name, file_name, source)

    # SourceCodeテーブルがなければ作成  
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SourceCode (  contract_address TEXT, contract_name TEXT, file_name TEXT, source TEXT)")
    
    # レコードの挿入
    sql = "INSERT INTO SourceCode VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (contract_address, contract_name, file_name, source))

    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()
  
def saveURLToDB(contract_address, contract_name, url):
    try:
        # RDSへの接続
        conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
    except Exception:
        print("DB CONNECTION ERROR at saveURLToDB")
        saveURLToDB(contract_address, contract_name, url)

    # URLテーブルがなければ作成  
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS URL (contract_address TEXT, contract_name TEXT, url TEXT)")
    
    # レコードの挿入
    sql = "INSERT INTO URL VALUES (%s, %s, %s)"
    cur.execute(sql, (contract_address, contract_name, url))
    
    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()

def saveContractInfoToDB(contract_address, contract_name, verified, CreationDate, BlockNumber, TelegramUsername, TelegramID):
    try:
        # RDSへの接続
        conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
    except Exception:
        print("DB CONNECTION ERROR at saveContractInfoToDB")
        saveContractInfoToDB(contract_address, contract_name, verified, CreationDate, BlockNumber, TelegramUsername, TelegramID)
    
    # ContractInfoテーブルがなければ作成
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ContractInfo (contract_address TEXT, contract_name TEXT, verified BOOLEAN, CreationDate TEXT, BlockNumber INTEGER,TelegramUsername TEXT,TelegramID TEXT)")

    # レコードの挿入 
    sql = "INSERT INTO ContractInfo VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (contract_address, contract_name, verified, CreationDate, BlockNumber, TelegramUsername, TelegramID))

    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()

def saveBlockNumberToDB(BlockNumber):
    try:
        # RDSへの接続
        conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
    except Exception:
        print("DB CONNECTION ERROR at saveBlockNumberToDB")
        saveBlockNumberToDB(BlockNumber)
    
    # ContractInfoテーブルがなければ作成
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS BlockNumber (BlockNumber INTEGER)")

    # レコードの挿入 
    sql = "INSERT INTO BlockNumber VALUES (%s)"
    cur.execute(sql, (BlockNumber,))

    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()

def makeContractSourceCode():
    # RDSへの接続
    conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)

    # SourceCodeテーブルがなければ作成  
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SourceCode (  contract_address TEXT, contract_name TEXT, file_name TEXT, source TEXT)")

    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()

def makeURL():
    # RDSへの接続
    conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
    # URLテーブルがなければ作成  
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS URL (contract_address TEXT, contract_name TEXT, url TEXT)")

    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()

def makeContractInfo():
    # RDSへの接続
    conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
    
    # ContractInfoテーブルがなければ作成
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ContractInfo (contract_address TEXT, contract_name TEXT, verified BOOLEAN, CreationDate TEXT, BlockNumber INTEGER,TelegramUsername TEXT,TelegramID TEXT)")
    
    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()

def makeBlockNumber():
    # RDSへの接続
    conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
    
    # ContractInfoテーブルがなければ作成
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS BlockNumber (BlockNumber INTEGER)")

    # コミットして閉じる
    conn.commit()
    cur.close()
    conn.close()
