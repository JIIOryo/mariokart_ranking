import datetime, json, requests

from bs4 import BeautifulSoup

# params ---
line_notify_url = 'https://notify-api.line.me/api/notify'
target_url = 'https://mariokarttour.com/ja-JP/ranking/allcup'
line_notify_token = ''
nickname = ''
previous_ranking_path = './latest_rank.json'
# ----------

def get_ranking():
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, 'lxml')

    return json.loads(
        soup.find('div', class_='page-ranking')['data-ranking']
    )


def get_previous_ranking():
    try:
        with open(previous_ranking_path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def set_latest_ranking(new_ranking):
    with open(previous_ranking_path, 'w') as f:
        json.dump(new_ranking, f, indent = 4)
    return


def get_ranking_period(ranking):
    return {
        'ranking_started_at': ranking[0]['ranking_started_at'],
        'ranking_finished_at': ranking[0]['ranking_finished_at'],
    }
    

def post_to_line_notify(message):
    r = requests.post(
        line_notify_url,
        headers = {
            'Authorization' : 'Bearer ' + line_notify_token
        },
        params = {
            'message': message
        }
    )


def date_format(date_str):
    datetime_utc = datetime.datetime.strptime( date_str.replace('.000Z', ''), '%Y-%m-%dT%H:%M:%S')
    datetime_jst = datetime_utc + datetime.timedelta(hours=+9)
    return datetime_jst.strftime('%m/%d %H:%M')


def post_message_generator(rank, score, ranking_started_at, ranking_finished_at, now):
    if rank == '0' and score == '0':
        ranking_message = 'ランキング圏外です。'
    else:
        ranking_message = '✨{rank}位 {score}点✨ '.format(rank = rank, score = score)

    return '''
ランキングが更新されました！

{nickname}さん
{ranking_message}

集計期間
{ranking_started_at} ~ {ranking_finished_at}
データ取得日時
{now}
    '''.format(
        nickname = nickname,
        ranking_message = ranking_message,
        ranking_started_at = ranking_started_at,
        ranking_finished_at = ranking_finished_at,
        now = now,
    )
    




def main():

    previous_ranking = get_previous_ranking()
    ranking = get_ranking()
    ranking_period = get_ranking_period(ranking)

    your_data = {
        'rank': '0',
        'score': '0',
        'ranking_started_at': ranking_period['ranking_started_at'],
        'ranking_finished_at': ranking_period['ranking_finished_at'],
    }

    for user_data in ranking:
        if user_data['nickname'] == nickname:
            your_data = user_data
            break

    if your_data != previous_ranking:
        # Ranking is updated
        set_latest_ranking(your_data)

        message = post_message_generator(
            rank = your_data['rank'],
            score = your_data['score'],
            ranking_started_at = date_format( ranking_period['ranking_started_at'] ),
            ranking_finished_at = date_format( ranking_period['ranking_finished_at']),
            now = datetime.datetime.now().strftime('%m/%d %H:%M'),
        )
        print(message)
        post_to_line_notify(message)
    else:
        # Ranking is not updated
        print('Not updated')



if __name__ == '__main__':
    main()
