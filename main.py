import json
from block import getContractAddresses, getLatestBlockNumberInDB, getLatestBlockNumberOnChain
from database import saveBlockNumberToDB, makeURL, makeContractSourceCode, makeBlockNumber, makeContractInfo
import time

blocks_per_day = (60*60*24)/10
blocks_per_week = 7 * blocks_per_day

def makeTable():
    # テーブル作成
    makeContractInfo()
    makeBlockNumber()
    makeContractSourceCode()
    makeURL()

def main():
    # コントラクトアドレスの取得
    latest_block_num = getLatestBlockNumberOnChain() - int(blocks_per_week)
    db_block_num = getLatestBlockNumberInDB()

    # DB内のブロックナンバーが0以上のときで、チェーン上の最新のブロックナンバーの方が大きければコントラクトアドレスを取得
    if db_block_num >= 0:
        if latest_block_num > db_block_num:
            getContractAddresses(db_block_num + 1, latest_block_num)
        else:
            return
    # DB内にブロックナンバーが存在しないとき、最新のブロックのコントラクトアドレスを取得
    else:
        getContractAddresses(latest_block_num, latest_block_num)

makeTable()
while(True):
    main()
    time.sleep(10)