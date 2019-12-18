# coding: utf-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_INFO = {
    'name': 'front_team_bot',
    'id': ''
}

#JIRA処理用
JIRA = {
    'url': os.environ.get('JIRA_URL'),
    'issue_url': os.environ.get('JIRA_URL_BROWSER'),
    'login_id': os.environ.get('JIRA_ID'),
    'login_pass': os.environ.get('JIRA_PASS'),
    'project': 'FTT',
    'issue_type_id': '10100',
    'ticket_kind': {
        '1': '調査',
        '2': '実装',
        '3': 'テストコード',
        '4': 'テスト仕様書',
        '5': 'レビュー',
        '6': 'レビュー指摘対応',
        '7': 'アップ作業',
        '8': 'iccheckテスト',
        '9': 'beforeテスト',
        '10': 'wwwテスト',
        '99': 'その他'
    }
}

# お昼休憩
BREAK = {
    os.environ.get('BREAK_FILE')
}

PATTERN = {
    'user_mention': r'^<@.*>$',
    'bot_mention' : r'^<@' + BOT_INFO['id'] + '>$',
    'date': r'^(\d{4})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])$',
    'ymd': '%Y%m%d',
    'y/m/d': '%Y/%m/%d'
}