# coding: utf-8

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot_settings import API_TOKEN
from service.slack_message_service import SlackMessageService
from service.file_service import FileService
import random
import schedule
import time
from threading import Timer,Thread,Event
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from pandas.tseries.offsets import BDay

class perpetualTimer():
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


def send_message_to_rel_front(message):
    slack_service = SlackMessageService(API_TOKEN)
    # rel_front_taskチャンネル
    slack_service.post_message('CME68B5MW', message)
    print('[rel_front_task]へ自動メッセージ送信[' + message + ']')


def send_message_to_rel(message):
    slack_service = SlackMessageService(API_TOKEN)
    # relチャンネル
    slack_service.post_message('CB0RQ8SAE', message)
    print('[rel]へ自動メッセージ送信[' + message + ']')


schedule.every().day.at('13:45').do(send_message_to_rel_front, '<@UAK1FG22Y> <@UD64F608P> \n*一回ぐらいみんなの進捗確認してちょ*:pray:\nhttps://ac-tech.rickcloud.jp/jira/secure/RapidBoard.jspa?rapidView=95&projectKey=FTT&quickFilter=373')

schedule.every().day.at('17:00').do(send_message_to_rel_front, '<!channel> \n*今日のTODOチケット終わりそうすか？？*\nそろそろチケット整理していこう！\nhttps://ac-tech.rickcloud.jp/jira/secure/RapidBoard.jspa?rapidView=95&projectKey=FTT&quickFilter=373')

schedule.every().day.at('17:15').do(send_message_to_rel_front, '<@UAK1FG22Y> <@UD64F608P> \n*ちゃんとみんなのチケット確認してね～*:sunglasses:\nhttps://ac-tech.rickcloud.jp/jira/secure/RapidBoard.jspa?rapidView=95&projectKey=FTT&quickFilter=373')


#rel全体用
schedule.every().thursday.at('17:15').do(send_message_to_rel, '<!channel> \n*明日は金曜日やから掃除やから8:30やで～*:face_vomiting:\n祝日やったりしたらスルーしてちょ。')


def check_last_day():
    today = (datetime.today()).date()
    last_month_day = (datetime.today().replace(day=1) + relativedelta(months=1, days=-1)).date()

    week_list = ['月', '火', '水', '木', '金', '土', '日']
    week = week_list[last_month_day.weekday()]

    if week == '土' or week == '日':
        last_month_day = (last_month_day - BDay(1)).date()

    msg = ''
    first_month_day = (last_month_day + BDay(1)).date()
    if today == last_month_day:
        msg += '<!channel> \n*' + first_month_day.strftime('%Y/%m/%d') + 'は月初やから8:30やで～*:face_vomiting:\n'\
                + '(朝会の時間に来てる人のために一応...)\n\n'

    send_message_to_rel(msg)


def check_first_day():
    today = (datetime.today()).date()
    first_month_day = (datetime.today().replace(day=1)).date()

    week_list = ['月', '火', '水', '木', '金', '土', '日']
    week = week_list[first_month_day.weekday()]

    if week == '土' or week == '日':
        first_month_day = (first_month_day + BDay(1)).date()

    msg = ''
    if today == first_month_day:
        msg += '<!channel> \n*月初は勤怠提出日なんで、川野さんにおっくてね～*\n'\
                + '\n> 提出方法\n'\
                + '```https://ac-tech.rickcloud.jp/wiki/pages/viewpage.action?pageId=310640933```\n'\
                + '\n> 川野さんメアド\n'\
                + '```yakawano@advancecreate.co.jp```\n'\
                + '\n> PDFファイル名\n'\
                + '```AC勤怠' + (first_month_day - BDay(1)).strftime('%Y%m') + '_氏名.pdf```\n'

    send_message_to_rel(msg)


schedule.every().day.at('17:15').do(check_last_day)
schedule.every().day.at('08:45').do(check_first_day)

# # 自動リマインド
def run_pending():
    schedule.run_pending()

notification = perpetualTimer(30, run_pending)
notification.start()


@respond_to(r'^.*vscode.*')
def get_vscode_cheet(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)
    slack_info.upload_file('./upload_files/vscode_cheat.jpg')
    msg = '*VSCodeマスターになろうぜ！！:computer:*'
    message.send(msg)


@listen_to(r'^.*vscode.*')
def get_vscode_cheet_listen(message):
    get_vscode_cheet(message)


@respond_to(r'^.*gitコマンド.*')
def get_git_cheet(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)
    slack_info.upload_file('./upload_files/git_cheat.jpg')
    msg = '*SouceTree使うよりコマンド来の方がかっこよくね？:ghost:*'
    message.send(msg)


@listen_to(r'^.*gitコマンド.*')
def get_git_cheet_listen(message):
    get_git_cheet(message)


@respond_to(r'^.*無駄.*')
def useless_replay(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)
    quote_list = [
        '人生に無駄なことは、なにひとつとしてない。',
        '自分のやってきたことは無駄じゃないと思いたい。',
        '人生に無駄なことがないのかは、僕たちには分からない。'
    ]
    message.send(random.choice(quote_list))


@listen_to(r'^.*無駄.*')
def useless_replay_listen(message):
    useless_replay(message)


@respond_to(r'^おらに元気を.*|^オラに元気を.*|^.*だめ.*|^.*ダメ.*|^.*元気.*|^.*やる気.*')
def oranigennkiwo_replay(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)
    yes_list = [
        '君にこの言葉をささげよう\n>>>壁というのは、\nできる人にしかやってこない。\n超えられる可能性がある\n人にしかやってこない。\nだから、壁がある時は\nチャンスだと思っている。 \n\nby イチロー',
        '君にこの言葉をささげよう\n>>>神様は私たちに、\n成功してほしいなんて思っていません。\nただ、挑戦することを望んでいるだけよ。 \n\nby マザーテレサ',
        '君にこの言葉をささげよう\n>>>過去ばかり振り向いていたのではダメだ。\n自分がこれまで何をして、\nこれまでに誰だったのかを受け止めた上で、\それを捨てればいい。\n\nby スティーブ・ジョブズ',
        '君にこの言葉をささげよう\n>>>私は失敗したことがない。\nただ、1万通りの、\nうまく行かない方法を\n見つけただけだ。\n\nby トーマス・エジソン',
        '君にこの言葉をささげよう\n>>>万策尽きたと思うな。\n自ら断崖絶壁の淵にたて。\nその時はじめて新たなる風は必ず吹く。\n\nby 松下幸之助',
        '君にこの言葉をささげよう\n>>>太陽の光と雲ひとつない青空があって、\nそれを眺めていられるかぎり、\nどうして悲しくなれるというの？\n\nby アンネ・フランク',
        'この映画全部見ればきっと元気になる！！！\nhttps://bibi-star.jp/posts/7801',
    ]
    message.send(random.choice(yes_list))


@listen_to(r'^おらに元気を.*|^オラに元気を.*|^.*だめ.*|^.*ダメ.*|^.*元気.*|^.*やる気.*')
def oranigennkiwo_listen(message):
    oranigennkiwo_replay(message)


@respond_to(r'^了解.*|^わかった.*|^わかりました.*|^ok.*|^OK.*|^承知.*|^りょうかい.*|^りょ.*|^おけ.*')
def yes_replay(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)
    yes_list = [
        '頼んます～。',
        'あざーす。',
        '君ならできる！',
        'You Can Do It!!!',
        '素敵やん',
        'よろしくっす～'
    ]
    message.send(random.choice(yes_list))


@listen_to(r'^了解.*|^わかった.*|^わかりました.*|^ok.*|^OK.*|^承知.*|^りょうかい.*|^りょ.*|^おけ.*')
def yes_replay_listen(message):
    yes_replay(message)


@respond_to(r'^ありがと.*|^あざ.*')
def thanks_replay(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)
    thanks_list = [
        'お安い御用っす',
        'いつでもゆうてな！'
    ]
    message.send(random.choice(thanks_list))


@listen_to(r'^ありがと.*|^あざ.*')
def thanks_replay_listen(message):
    thanks_replay(message)


@respond_to(r'^.*完了.*|^.*終わ.*|^.*おわ.*')
def done_replay(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)
    done_list = [
        'やるやんっ',
        'さすが！',
        '天才',
        'いいね！',
        '僕の仕事も手伝ってw'
    ]
    message.send(random.choice(done_list))


@listen_to(r'^.*完了.*|^.*終わ.*|^.*おわ.*')
def done_replay_listen(message):
    done_replay(message)