# coding: utf-8
from slackclient import SlackClient
from slacker import Slacker

class SlackMessageService:

    '''
     slack関連の処理クラス
    '''

    def __init__(self, token, message = None):

        '''
        : summary : 初期処理
        : param   : token (BOTのトークン)
        : param   : message (メッセージオブジェクト)
        '''

        self.token = token
        if message is not None:
            self.message = message
            self.message_text = message.body['text']
            self.user = self.get_user()
            self.user_id = self.user['id']
            self.base_login_id = self.user['name']
            self.user_info = self.user['profile']
            self.user_name = self.get_user_name()
            self.email = self.user_info['email']


    def upload_file(self, file_path):

        '''
        : summary : ファイルアップロード
        : param   : アップロードファイルのパス
        '''

        slacker = Slacker(self.token)
        slacker.files.upload(file_= file_path, channels = self.message.body['channel'])


    def get_user(self, user_id = None):

        '''
        : summary : メッセージからユーザ情報取得
        : return  : user (ユーザ情報)
        '''

        sc = SlackClient(self.token)
        if (user_id):
            user = user_id
        else:
            user = self.message.body['user']
        user = sc.api_call(
            'users.info',
            user = user
        )
        return user['user']


    def get_user_name(self):

        '''
        : summary : 表示名をユーザ名として返す。表示名が登録されていなければ、氏名を返す。
        : return  : user_name (ユーザ名))
        '''

        user_name = self.user_info['display_name']
        if (len(user_name) == 0):
            user_name = self.user_info['real_name']
        return user_name


    def post_message(self, channel_id, msg_text):

        '''
        : summary : 特定ユーザへダイレクトメッセージを送る
        : param   : channel_id (チャンネル_ID)
        : param   : msg_text (送信メッセージ)
        '''

        sc = SlackClient(self.token)
        sc.api_call(
            'chat.postMessage',
            as_user = 'front_team_bot',
            channel = channel_id,
            text = msg_text
        )