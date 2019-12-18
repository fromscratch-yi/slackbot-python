# coding: utf-8
import json
import codecs
import os.path
import datetime

class FileService:

    '''
     ファイル処理クラス
    '''

    def get_json_file_data(self, file_path):

        '''
        : summary : jsonファイルのデータ取得
        : param   : file_path (ファイルパス)
        : return  : data_list (jsonのデータリスト)
        '''

        if (os.path.exists(file_path)
            and os.path.getsize(file_path) > 0):
            file_data = codecs.open(file_path, 'r', 'utf-8')
            data_list = json.load(file_data)
            file_data.close()
        else:
            data_list = []

        return data_list


    def write_json_file(self, file_path, data_list):

        '''
        : summary : jsonデータをファイルに書き込み
        : param   : file_path (ファイルパス)
        : param   : data_list (書き込みデータリスト)
        '''

        file_data = codecs.open(file_path, 'w', 'utf-8')
        json.dump(data_list, file_data, indent=4, sort_keys=True,
                      ensure_ascii=False)
        file_data.close()

    @classmethod
    def write_log(self, user_name, user_id, message_text):

        '''
        : summary : ログメッセージを追記する
        : param   : msg_text (ログメッセージ)
        '''
        log_msg = user_name + '（' + user_id + '）' + '[Message :' + message_text + ']'
        print(log_msg)
        log_file = codecs.open('./log.txt', 'a', 'utf-8')
        log_file.write('【' + str(datetime.datetime.today()) + '】' + str(log_msg) + '\n')
        log_file.close()
