import asyncio
import configparser
import sys
import requests
import json
from web3 import Web3
from utils import extractURLs
from telegram import getTelegramUsername, getTelegramID
from database import saveURLToDB, saveContractSourceCodeToDB, saveContractInfoToDB, saveBlockNumberToDB
import psycopg2
import datetime

# APIキーやRDSの情報を設定ファイルから読み込む
config = configparser.ConfigParser()
config.read('config/config.ini')
etherscan_api_key = config.get('etherscan', 'api_key')
infura_api_key = config.get('infura', 'api_key')
ENDPOINT = config.get('rds', 'endpoint')
PORT = config.get('rds', 'port')
DATABASE = config.get('rds', 'database_name')
USERNAME = config.get('rds', 'username')
PASSWORD = config.get('rds', 'password')

# 指定されたブロック間のContract Creation Transactionのハッシュを取得し、コントラクトアドレスを取得
def getContractAddresses(start_block, end_block):
    # Ethereumノードに接続
    w3 = Web3(Web3.HTTPProvider('https://cloudflare-eth.com'))
    for i in range(start_block, end_block + 1):
        try:
            block = w3.eth.get_block(i, full_transactions=True)
            print(f'Current block       : {i}')
            if block:
                for tx in block.transactions:
                    if tx['to'] is None:
                        # HexBytesオブジェクトを文字列に変換
                        tx_hash_str = tx['hash'].hex()
                        print(f"Contract Creation Tx: {tx_hash_str}")
                        receipt = w3.eth.get_transaction_receipt(tx['hash'])
                        if receipt:
                            contract_address = receipt['contractAddress']
                            print(f'Contract address    : {contract_address}')

                            getContractInfo(contract_address, i)

            saveBlockNumberToDB(i)
            sys.stdout.flush()

        except Exception as e:
            print(e)

# Etherscan APIで最新のブロックナンバーを取得
def getLatestBlockNumberOnChain():
    try:
        response = requests.get(f"https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey={etherscan_api_key}")
        data = response.json()
        return int(data.get("result"), 16)

    except requests.exceptions.RequestException as e:
        return getLatestBlockNumberOnChain()
    
# DB中の最新のブロックナンバーを取得
def getLatestBlockNumberInDB():
    try:    
        conn = psycopg2.connect(host=ENDPOINT, database=DATABASE, user=USERNAME, password=PASSWORD, port=PORT)
        cur = conn.cursor()
        # BlockNumber TableからBlockNumberの最大値を取得
        cur.execute("SELECT MAX(BlockNumber) FROM BlockNumber") 
        max_block_num = cur.fetchone()[0]
        conn.close()
        if(max_block_num):
            return max_block_num
        else:
            return -1
    
    except Exception as e:
        print(e)
        return -1

# ソースコードのレスポンスを取得
def getEtherscanGetSourceCodeResponse(contract_address):
    response = requests.get(f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={contract_address}&apikey={etherscan_api_key}")
    if response.status_code != 200:
        raise Exception(f"Failed Response from API. Status Code: {response.status_code}")
    return response

# レスポンスからソースコードを取得
def getSourceCode(response):
    file_dict = {}
    try:
        # Get source code JSON from the response JSON string
        response_json1 = response.json()["result"][0]["SourceCode"][1:-1]

        # 複数のファイルから構成されている場合
        if  "\"language\":" in response_json1 or ":{\"content\":" in response_json1: 
            if "sources" in response_json1 :
                # Load sources from SourceCode JSON
                response_json2 = json.loads(response_json1)["sources"]
                # これは名前のリスト
                sources_list = [contract for contract in response_json2]

                # 辞書型に保存
                for source in sources_list:
                    file_dict[source] = response_json2[source]['content']

                return file_dict, True
                        
            else :
                response_json3 = response.json()["result"][0]["SourceCode"]
                data = json.loads(response_json3)

                # 辞書型に保存
                for name, source in data.items():
                    file_dict[name] = source['content']
                return file_dict, True

        # 1つのファイルから構成されている場合
        else : 
            # ソースコードがないとき
            if response.json()["result"][0]["SourceCode"] == "":
                return file_dict, False
            
            # ソースコードがあるとき
            file_dict[response.json()["result"][0]["ContractName"] + ".sol"] = response.json()["result"][0]["SourceCode"]
            return file_dict, True
        
    except Exception as e:
        print(e)
        return file_dict, False

# レスポンスからコントラクトネームを取得
def getContractName(response):
    try:
        contract_name = response.json()["result"][0]["ContractName"]
    except:
        return ""
    return contract_name

# ブロックナンバーからコントラクトの作成日時を取得
def getContractTimestamp(block_num):
    block_num = hex(block_num)
    # Etherscan APIのエンドポイントURL
    url = f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag={block_num}&boolean=true&apikey={etherscan_api_key}'
    # APIリクエストを送信
    response = requests.get(url)
    # レスポンスをJSON形式にパース
    data = response.json()
    # ブロックのタイムスタンプを取得
    timestamp = int(data['result']['timestamp'], 16)
    # タイムスタンプを人間が読める形式に変換
    block_time = datetime.datetime.utcfromtimestamp(timestamp)
    return block_time

# コントラクトの情報を全て取得する
def getContractInfo(contract_address, block_num):
    try:
        # レスポンスを取得
        response = getEtherscanGetSourceCodeResponse(contract_address)
        contract_name = getContractName(response)
        sources_dict, verified = getSourceCode(response)
        CreationDate = getContractTimestamp(block_num)
        BlockNumber = block_num
    except Exception as e:
        print(e)
        return False
    
    # 扱いやすいようにソースコードを全て連結
    all_source_code = ""
    for source in sources_dict.values():
        all_source_code += source

    # ソースコードのテーブルに保存
    for file_name, source in sources_dict.items():
        saveContractSourceCodeToDB(contract_address, contract_name, file_name, source)

    # URLのテーブルに保存
    urls = extractURLs(all_source_code)
    for url in urls:
        saveURLToDB(contract_address, contract_name, url)

    # Telegramのユーザネームを取得
    TelegramUsername = getTelegramUsername(all_source_code)

    # TelegramのIDを取得
    if(TelegramUsername):
        TelegramID = asyncio.run(getTelegramID(TelegramUsername))
    else:
        TelegramID = ""

    # Contractのテーブルに保存
    saveContractInfoToDB(contract_address, contract_name, verified, CreationDate, BlockNumber, TelegramUsername, TelegramID)
    
    return True