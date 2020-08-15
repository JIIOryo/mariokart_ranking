from datetime import datetime
import json

from bs4 import BeautifulSoup

from .consts import LINE_MESSAGE_TEMPLATE

class Ranking:
    def __init__(
        self,
        target_url: str,
        previous_ranking_path: str,
        use_example: bool = False
    ):
        self.target_url = target_url
        self.previous_ranking_path = previous_ranking_path
        self.use_example = use_example

    def __get_html(self) -> None:
        if self.use_example:
            # example.htmlをセット
            from .html_downloader import html_example
            html = html_example()
            self.html = html
            return

        # headressのchromeを利用してダウンロードしたhtmlをセット
        from .html_downloader import html_download_by_chrome
        html = html_download_by_chrome(self.target_url)
        self.html = html
        return

    def __scrape_ranking(self) -> dict:
        soup = BeautifulSoup(self.html, 'lxml')
        return json.loads(
            soup.find('div', class_='page-ranking')['data-ranking']
        )

    def __scrape_schedule_period(self) -> str:
        soup = BeautifulSoup(self.html, 'lxml')
        schedule_period = soup.find('p', class_='schedule-period').text
        return self.__format_schedule_period(schedule_period)
    
    def __format_schedule_period(self, schedule_period: str) -> dict:
        # schedule_period = '2020/08/12 15:00 - 2020/08/14 00:00'
        start_end = schedule_period.split(' - ')
        return {
            'start': start_end[0],
            'end': start_end[1],
        }

    def previous(self) -> dict:
        try:
            with open(self.previous_ranking_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def latest(self, nickname: str) -> dict:
        self.__get_html()
        all_ranking = self.__scrape_ranking()

        ranking = {
            'my_ranking': {
                'nickname': nickname,
                'rank': '0',
                'score': '0',
            },
            'schedule_period': self.schedule_period()
        }

        for user_ranking in all_ranking:
            if user_ranking['nickname'] == nickname:
                ranking['my_ranking']['rank'] = user_ranking['rank']
                ranking['my_ranking']['score'] = user_ranking['score']
                break
        
        return ranking
    
    def save(self, ranking) -> None:
        with open(self.previous_ranking_path, 'w') as f:
            json.dump(ranking, f, indent = 4, ensure_ascii = False)
        return
    
    def schedule_period(self) -> dict:
        '''
        {'start':'2020/08/12 15:00','end':'2020/08/14 00:00'}
        '''
        return self.__scrape_schedule_period()

def line_message_generator(
    nickname: str,
    rank: str,
    score: str,
    ranking_started_at: str,
    ranking_finished_at: str,
    now: str = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
):
    ranking_message = 'ランキング圏外です。'
    if rank != '0' or score != '0':
        ranking_message = f'✨{rank}位 {score}点✨ '

    return LINE_MESSAGE_TEMPLATE.format(
        nickname = nickname,
        ranking_message = ranking_message,
        ranking_started_at = ranking_started_at,
        ranking_finished_at = ranking_finished_at,
        now = now,
    )
