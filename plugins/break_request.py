# coding: utf-8

from slackbot.bot import respond_to
from slackbot_settings import API_TOKEN
from const_msg import BREAK_MSG
from const import BREAK
from service.slack_message_service import SlackMessageService
from service.file_service import FileService
from service.break_service import BreakService


@respond_to(r'^.*休憩.*|^.*昼.*')
def get_break_time(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)

    message.send(create_break_msg())


def create_break_msg():

    '''
    : summary : チーム別の休憩時間を取得し、返信メッセージを作成する。
    : param   : team_name (チーム名)
    : return  : msg (返信メッセージ)
    '''

    msg = ''
    break_service = BreakService()
    break_info = break_service.get_break_list(BREAK['break_excel'])
    msg = BREAK_MSG['title'].format(break_info['date'])

    if not break_info:
        msg = BREAK['not_get_break']
    else:
        idx = 0
        for user_list in break_info['user_list']:
            msg +=  BREAK_MSG['break_time'][idx]
            idx += 1
            for user in user_list:
                msg += BREAK_MSG['user_name'].format(user)

    return msg