## mariokart_ranking

マリオカートツアーの[オールカップランキング](https://mariokarttour.com/ja-JP/ranking/allcup)における
特定のユーザのランキングを取得してLINE Notifyで通知するスクリプト

## 環境構築

```
sh init.sh
```

## 動作環境

```
python3.6
Ubuntu 18.04.2 LTS
```

## 定期実行

以下の実行結果をcronに登録しておくと便利
```
echo "*/15 * * * * cd `pwd` && python3 main.py"
```

