# coding: utf-8

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot_settings import API_TOKEN
from const_msg import JIRA_MSG
from const import JIRA, PATTERN
from service.slack_message_service import SlackMessageService
from service.file_service import FileService
from service.jira_service import JiraService
import re

@respond_to('報告チケット')
def get_report_ticket(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)

    jira_service = JiraService(JIRA['url'], JIRA['login_id'], JIRA['login_pass'])
    tickets = jira_service.get_incompleate_ticket(
        jira_service.get_report_ticket(JIRA['project'], slack_info.base_login_id)
    )
    if len(tickets) == 0:
        msg = JIRA_MSG['not_report_ticket'].format(slack_info.user_name)
    else:
        msg = JIRA_MSG['get_report_ticket'].format(slack_info.user_name)
        msg += create_get_ticket_msg(jira_service, tickets)

    message.send(msg)


@respond_to('担当チケット')
def get_assignee_ticket(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    user_name = slack_info.user_name
    FileService.write_log(user_name, slack_info.user_id, slack_info.message_text)

    jira_service = JiraService(JIRA['url'], JIRA['login_id'], JIRA['login_pass'])
    msg_list = slack_info.message_text.split()
    msg_len = len(msg_list)
    user_id = slack_info.base_login_id

    if (msg_len > 1):
        user_mention = msg_list[1]
        if re.match(PATTERN['user_mention'], user_mention):
            user_mention = user_mention.lstrip('<@')
            user_mention = user_mention.rstrip('>')
            user_info = slack_info.get_user(user_mention)
            user_id = user_info['name']
            user_name = user_info['profile']['display_name']

    tickets = jira_service.get_incompleate_ticket(
        jira_service.get_assignee_ticket(JIRA['project'], user_id)
    )

    if len(tickets) == 0:
        msg = JIRA_MSG['not_assignee_ticket'].format(user_name)
    else:
        msg = JIRA_MSG['get_assignee_ticket'].format(user_name)
        msg += create_get_ticket_msg(jira_service, tickets)

    message.send(msg)


@respond_to('チケット作成')
def create_task_ticket(message):
    slack_info = SlackMessageService(API_TOKEN, message)
    FileService.write_log(slack_info.user_name, slack_info.user_id, slack_info.message_text)

    jira_service = JiraService(JIRA['url'], JIRA['login_id'], JIRA['login_pass'])
    msg_list = slack_info.message_text.split()
    msg_len = len(msg_list)
    if msg_len == 3:
        kind = msg_list[1]
        title = msg_list[2]
        kind_list = kind.split(',')
        msg = JIRA_MSG['create_ticket']
        error_msg = ''
        for kind in kind_list:
            if (kind in JIRA['ticket_kind']):
                summary = '【' + JIRA['ticket_kind'][kind] + '】' + title
                ticket = jira_service.create_tickets(JIRA['project'], JIRA['issue_type_id'], summary, slack_info.base_login_id)
                msg += JIRA_MSG['create_ticket_list'].format(
                    summary = summary,
                    url = JIRA['issue_url'] + str(ticket)
                )
            else:
                error_msg += JIRA_MSG['kind_error'].format(str(kind))
        msg += error_msg
    else:
        msg = JIRA_MSG['help']

    message.send(msg)


@listen_to(r'^報告チケット$')
def get_report_ticket_listen(message):
    get_report_ticket(message)


@listen_to(r'^担当チケット.*')
def get_assignee_ticket_listen(message):
    get_assignee_ticket(message)


@listen_to(r'^チケット作成.*')
def create_task_ticket_listen(message):
    create_task_ticket(message)


def create_get_ticket_msg(jira_service, tickets):

    '''
    : summary : チケット取得返信用メッセージの作成
    : param   : jira_service (Jiraオブジェクトのインスタンス)
    : param   : tickets (チケットオブジェクト)
    : return  : msg (返信メッセージ)
    '''

    msg = ''
    for ticket in tickets:
        msg += JIRA_MSG['get_ticket_list'].format(
            summary = jira_service.get_ticket_summary(ticket),
            status = jira_service.get_ticket_status(ticket),
            url = JIRA['issue_url'] + str(ticket)
        )
    return msg
