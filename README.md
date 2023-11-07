# Contract SNS Monitoring System

## 概要
Ethereumブロックチェーンにおいて、新しく作成されたコントラクトのソースコードからSNSのURLを抽出し、AWSのRDSに保存する。SNSの監視及びフィルタリング機能を追加予定。こちらはLinux環境での実行を想定。
実行には`config/config.ini`にAPIキーやRDSの設定が必要。

## 使用方法
通常：
```
python main.py
```
Linuxのバックグラウンドで実行する場合：
```
nohup python main.py > nohup.out &
```
を実行した後、以下のコマンドでログを確認する。
```
tail -f -n 10 nohup.out
```

`config/excluded_words.txt`には除外するURLに含まれる文字列を入力する。

## 保存される情報
- ContractInfoテーブル
  - ConractAddress, ContractName, CreationDate, Verified(Boolean), BlockNumber, TelegramID, ChatID
- URLテーブル
  - ContractAddress, ContractName, URL
- Sourceテーブル
  - ContractAddress, ContractName, filename, source
- BlockNumberテーブル
  - BlockNumber

## TODO
- Telegramのメッセージの保存ロジックを追加
- Twitterの投稿検索ロジックを追加
- メッセージのフィルタリングロジックを追加
