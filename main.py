
from bs4 import BeautifulSoup

from lib.consts import (
    CONFIG_PATH,
    PREVIOUS_RANKING_PATH,
    RANKING_URL,
)
from lib.config import get_config
from lib.ranking import (
    Ranking,
    line_message_generator,
)
from lib.line import post_to_line_notify

def main():
    config = get_config(CONFIG_PATH)
    
    ranking = Ranking(
        target_url = RANKING_URL,
        previous_ranking_path = PREVIOUS_RANKING_PATH,
    )

    latest_my_ranking = ranking.latest(nickname = config['nickname'])
    previous_my_ranking = ranking.previous()

    if latest_my_ranking == previous_my_ranking:
        print('not updated')
        return
    
    ranking.save(latest_my_ranking)
    print(latest_my_ranking)

    line_message = line_message_generator(
        nickname = latest_my_ranking['my_ranking']['nickname'],
        rank = latest_my_ranking['my_ranking']['rank'],
        score = latest_my_ranking['my_ranking']['score'],
        ranking_started_at = latest_my_ranking['schedule_period']['start'],
        ranking_finished_at = latest_my_ranking['schedule_period']['end'],
    )

    post_to_line_notify(
        message = line_message,
        token = config['line_notify_token']
    )

if __name__ == '__main__':
    main()
