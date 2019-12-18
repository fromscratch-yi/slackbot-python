# coding: utf-8
from jira import JIRA
from jira.client import JIRA

class JiraService:

    '''
     Jira処理クラス
    '''

    def __init__(self, jira_url, jira_id, jira_pass):

        '''
        : summary : 初期処理
        : param   : jira_url (JiraのURL)
        : param   : jira_id (JiraログインID)
        : param   : jira_pass (JiraログインPASS)
        '''

        options = {
            'server': jira_url
        }
        self.jira = JIRA(options, basic_auth=(jira_id, jira_pass))


    def create_tickets(self, project, issue_type_id, summary, login_id):

        '''
        : summary : チケット作成
        : param   : login_id (ログインID)
        : param   : summary (サマリー)
        : return  : ticket (新規チケットオブジェクト)
        '''

        issue_dict = {
            'project': {'key': project},
            'summary': summary,
            'description':  summary,
            'issuetype': {'id': issue_type_id},
            'reporter': {'name': login_id},
            'assignee': {'name': login_id}
        }
        ticket = self.jira.create_issue(fields=issue_dict)
        return ticket


    def get_report_ticket(self, project, login_id):

        '''
        : summary : 報告チケット取得
        : param   : login_id (ログインID)
        : return  : tickets (チケットリスト)
        '''

        tickets = self.jira.search_issues('project=' + project + ' and reporter = ' + login_id)
        return tickets


    def get_assignee_ticket(self, project, login_id):

        '''
        : summary : 担当チケット取得
        : param   : login_id (ログインID)
        : return  : tickets (チケットリスト)
        '''

        tickets = self.jira.search_issues('project=' + project + ' and assignee = ' + login_id)
        return tickets


    def get_incompleate_ticket(self, tickets):

        '''
        : summary : 未完了チケットの取得
        : param   : tickets (Jiraチケットオブジェクトリスト)
        : return  : incomplete_tickets (未完了チケットリスト)
        '''

        incompleate_tickets = []
        for ticket in tickets:
            if (self.get_ticket_status(ticket) != '完了'
                and self.get_ticket_status(ticket) != '却下'):
                incompleate_tickets.append(ticket)
        return incompleate_tickets


    def get_ticket_summary(self, ticket):

        '''
        : summary : チケット要件の取得
        : param   : ticket (Jiraチケットオブジェクト)
        : return  : ticket.fields.summary (チケット要件)
        '''

        return str(ticket.fields.summary)


    def get_ticket_status(self, ticket):

        '''
        : summary : チケットステータスの取得
        : param   : ticket (Jiraチケットオブジェクト)
        : return  : ticket.fields.summary (チケット要件)
        '''

        return str(ticket.fields.status)

    def get_ticket_project(self, ticket):

        '''
        : summary : チケットのプロジェクト名の取得
        : param   : ticket (Jiraチケットオブジェクト)
        : return  : ticket.fields.summary (チケット要件)
        '''

        return str(ticket.fields.project)