
CONFIG_PATH = './config.json'

RANKING_URL = 'https://mariokarttour.com/ja-JP/ranking/allcup'
PREVIOUS_RANKING_PATH = './latest_rank.json'

LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
LINE_MESSAGE_TEMPLATE = '''
ランキングが更新されました！

{nickname}さん
{ranking_message}

集計期間
{ranking_started_at} ~ {ranking_finished_at}
データ取得日時
{now}
'''
