import gspread
from google.oauth2.service_account import Credentials
import pandas as pd


class GSC:
    def __init__(self, sid, key="/home/akumar/.alfred/credentials.json", w=0):
        self.sid            =   sid
        self.key            =   key
        self.w              =   w

        self.scopes         =   ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds          =   Credentials.from_service_account_file(key, scopes=self.scopes)
        
    def auth(self):
        self.client         =   gspread.authorize(self.creds)

    def open(self):
        self.workbook       =   self.client.open_by_key(self.sid)
        self.sheet          =   self.workbook.get_worksheet(self.w)
        self.df             =   pd.DataFrame(self.sheet.get_all_records())
        print("Success!")
        return self.df

    def update(self, dataframe):
        self.sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        print("Updated!")