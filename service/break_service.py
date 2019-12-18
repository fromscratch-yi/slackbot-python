# coding: utf-8
import pandas as pd
from datetime import date, datetime

class BreakService:

    '''
     お昼休憩取得用クラス
    '''

    def get_break_list(self, file_path):

        '''
        : summary : チーム別の休憩時間を取得する。
        : param   : file_path (損保or生保の休憩資料のパス)
        : return  : break_data_dict (休憩情報リスト)
        '''

        break_data_dict = {}

        excel = pd.ExcelFile(file_path, encoding = 'utf-8')
        sheet = excel.sheet_names
        sheetdf = excel.parse(sheet_name = sheet, skiprows = [0,1,2,3,4,7])

        data = ''
        for key, item in sheetdf.items():
            data = item.iloc[0:10, 1:4][item.iloc[0:10, 1:4].notnull().any(1)]
            data = data.dropna(how = 'all', axis = 1)

        idx = 0
        user_list = []
        time_list = []
        for key, item in data.iteritems():
            for item_data in item:
                if type(item_data) is str and idx == 0:
                    user = str(item_data) + 'さん'
                    user_list.append(user)
                elif isinstance(item_data, datetime):
                    break_data_dict['date'] = str(item_data.strftime('%Y/%m/%d'))
                elif type(item_data) is str and idx == 1:
                    time = str(item_data)
                    time_list.append(time)
            idx += 1

        if len(user_list) == len(time_list):
            break_user_list = []
            first_list = []
            latter_list = []

            for i in range(len(user_list)):
                if user_list[i] == '' or user_list[i] == '‐さん':
                    continue
                elif time_list[i] == '早':
                    first_list.append(user_list[i])
                elif time_list[i] == '遅':
                    latter_list.append(user_list[i])

            break_user_list.append(first_list)
            break_user_list.append(latter_list)
            break_data_dict['user_list'] = break_user_list
        return break_data_dict