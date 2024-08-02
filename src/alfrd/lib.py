import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import re, time
from pathlib import Path
import warnings
from alfrd import c
from gspread_formatting import ConditionalFormatRule, GridRange, BooleanCondition, BooleanRule, CellFormat, Color, get_conditional_format_rules

class GSC:
    """
    Creates instance of google Google Spreadsheet Credential to open and update a worksheet
    """
    def __init__(self, sid='', url='', key=f"{Path().home()}/.alfred/credentials.json", wid=0, wname=''):
        """
        if sid is empty, uses url to get the spreadsheet id
        """
        self.sid            =   sid
        self.url            =   url
        self.key            =   key
        self.wid            =   wid
        self.wname          =   wname
        self.authorized     =   False
        self.scopes         =   ["https://www.googleapis.com/auth/spreadsheets"]
        self.creds          =   Credentials.from_service_account_file(key, scopes=self.scopes)
        
    def auth(self):
        self.client         =   gspread.authorize(self.creds)
        self.authorized     =   True

    def open(self):
        if not self.authorized: self.auth()
        if not self.sid: 
            regex = "([\w-]){44}"
            sid_match = re.search(regex,self.url)
            self.sid = str(sid_match.group())

        self.spreadsheet    =   self.client.open_by_key(self.sid)
        self.sheet          =   self.spreadsheet.get_worksheet(self.w) if not self.wname else self.spreadsheet.worksheet(self.wname)
        self.df             =   pd.DataFrame(self.sheet.get_all_records(numericise_ignore=['all']))
        print(f"{c['g']}Success!{c['x']}")
        return self.df

    def update(self, dataframe):
        self.sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
        print(f"{c['g']}Updated!{c['x']}")

class LogFrame:
    """
    Input
    ---

    :gsc:               Google Spreadsheet Credentials instance
                        To use a local dataframe, initialize with lf = LogFrame(gsc = my_df ,....) and lf.df_sheet = my_df
    :primary_value:     the unique identifier of the row corrosponding to the primary_colname
    :primary_colname:     primary column name for unique identifier
    :registered:        keeps count of success and failed script runs in a tuple (count_success, count_failed)

    TODO :  register scripts to be able to call them from the terminal \
            e.g:
            $ alfrd --register alfred-pipe.py
            $ alfrd --step_name

    """
    def __init__(self, gsc , primary_value='',  primary_colname='FILE_NAME'):
        self.gsc                =   gsc
        self.df_sheet           =   self.gsc.df
        self.primary_value      =   primary_value
        self.primary_colname    =   primary_colname
        self.working_col        =   ''
        self.working_cols       =   []
        self.t0                 =   time.time()
        

        self.registered         =   0,0         # (count_success, count_failed)
        self.update_cooldown_count   =   0
        self.color ={'g': Color(red=0.56,green=0.77,blue=0.49),
                'r': Color(red=0.8784314,green=0.4,blue=0.4),
                'rh': Color(red=0.71,green=0.13,blue=0.0),
                'rl': Color(red=0.98,green=0.63,blue=0.57),
                'gl': Color(red=0.42,green=0.86,blue=0.31),
                'gh': Color(red=0.42,green=0.60,blue=0.42)}

    def col_data(self, colname='', data='', count=0, force=False, chk_colname=''):
        """
        program to change the column data of dataframe
        checks if primary_value exist and then change the value for empty cell with the given data.
        
        set primary_colname - primary column name to find unique values corrosponding to the primary_value e.g fitsfile name

        Input
        ---

        :df_sheet:          pandas dataframe to work on
        :primary_value:     the unique identifier of the row corrosponding to the primary_colname
        :colname:           column name to alter data
        :data:              data to fill in the corrosponding column for the corrosponding identifier row
        :count:             iterative count
        :force:             to force change the data in the column even if the cell is not empty.
        :primary_colname:     primary column name for unique identifier
        :chk_colname:       column name to check value for, if this is given no data is changed.

        Returns
        ---

        count if chk_column is empty; 

        (count, column_value) corrosponding to the `chk_colname`
        """
        colname = self.working_col if not colname else colname
        if not self.primary_value : print(f"{c['y']}No primary value given{c['x']}")
        primary_col_values     = self.df_sheet[self.primary_colname].str.strip()
        if (not force) or (primary_col_values.isin([self.primary_value]).any() and not self.df_sheet.loc[primary_col_values==self.primary_value,colname].count()):
            
            if chk_colname :
                if self.df_sheet.loc[primary_col_values==self.primary_value,chk_colname].count(): 
                    val = str(self.df_sheet.loc[primary_col_values==self.primary_value,chk_colname].values[0]).strip()
                    count+=1
                    return count, val 
                else:
                    return count, ''
            else:
                count+=1 
                self.df_sheet.loc[primary_col_values==self.primary_value,colname] = data
        else:
            print("not updating", self.primary_value, f"{self.df_sheet.loc[primary_col_values==self.primary_value,colname].values}")
        return count
    
    def isval_unique(self, colname=''):
        """
        checks if the colname has unique values and returns boolean
        """
        colname = self.working_col if not colname else colname
        _, colv = self.col_data(colname='', data='', count=0, chk_colname=colname)
        c = self.df_sheet[colname].value_counts()[colv]
        r = False if int(c)!=1 else True
        return r
    
    def get_value(self, colname=''):
        """
        gives the cell value for the colname returns string value
        """
        colname = self.working_col if not colname else colname
        _, colv = self.col_data(colname='', data='', count=0, chk_colname=colname)
        r = str(colv).strip()
        return r
    
    def get_previous_working_col(self):
        prev_col = None
        if len(self.working_cols)>=2 and (self.working_col in self.working_cols):
                pcol_idx    =   (self.working_cols).index(self.working_col) - 1
                prev_col = self.working_cols[pcol_idx] if pcol_idx!=-1 else None

        return prev_col
    
    def isvalue(self, value, colname=''):
        """
        Returns boolean by matching value in cell
        """
        colname = self.working_col if not colname else colname
        v = self.get_value(colname)
        return str(value) == str(v)
    
    def put_value(self, value, colname='', count=0):
        """
        puts value to the colname if specified else uses working_col for the colname
        returns +1 for the counter value
        Note: This only modifies data in the DataFrame
        """
        colname = self.working_col if not colname else colname
        count = self.col_data(colname=colname, data=value, count=count)
        return count
    
    def update_sheet(self, count, failed, comment_col='Comment4', csvfile = 'df_sheet.csv'):
        """
        updates the google sheet if there is atleast one new count/failed count for the update
        """
        # -----  Cool down update to keep it below 60 request/minute
        tf                          =   time.time()
        td                          =   tf-self.t0

        if td<=1 and (self.update_cooldown_count >=  1) and (count - self.registered[0] or failed - self.registered[1]):
            time.sleep(1)
            self.update_cooldown_count   =   0
            
        try:
            if count - self.registered[0] or failed - self.registered[1]:
                self.gsc.update(self.df_sheet)
                self.update_cooldown_count       +=  1
                self.registered = count, failed       
            else:
                print('skipped')
        except Exception as e:
            print(f'failed to update on google sheet: {e}')
            failed  =   self.col_data(colname=comment_col, data=f'failed:{e}', count=failed)
            self.df_sheet.to_csv(csvfile)
        self.t0                      =   time.time()

    def create_conditional_format(self, range, c='g', valtype='timeinmin', custom_clr=None):
        clr = self.color[c] if not custom_clr else custom_clr
        rule ={
                'timeinmin' : ConditionalFormatRule(
            ranges=[GridRange.from_a1_range(f'{range}', self.gsc.sheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition(
                        type='CUSTOM_FORMULA',values=[f'=AND(ISNUMBER(SEARCH("m", {range})), ISNUMBER(SEARCH("s", {range})))']),
                format=CellFormat(backgroundColor=clr,
                ))),
                'True' :  ConditionalFormatRule(
            ranges=[GridRange.from_a1_range(f'{range}', self.gsc.sheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition(
                        type='TEXT_CONTAINS',values=[f'True']),
                format=CellFormat(backgroundColor=clr,
                ))),
                'False' :  ConditionalFormatRule(
            ranges=[GridRange.from_a1_range(f'{range}', self.gsc.sheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition(
                        type='TEXT_CONTAINS',values=[f'False']),
                format=CellFormat(backgroundColor=clr,
                ))),
                'fail' :  ConditionalFormatRule(
            ranges=[GridRange.from_a1_range(f'{range}', self.gsc.sheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition(
                        type='TEXT_CONTAINS',values=[f'fail']),
                format=CellFormat(backgroundColor=clr,
                ))),
        }
        return rule[valtype]

    def create_rule(self, range, type='TEXT_CONTAINS', value='True',  c='g', custom_clr=None):
        clr = self.color[c] if not custom_clr else custom_clr
        return ConditionalFormatRule(
            ranges=[GridRange.from_a1_range(f'{range}', self.gsc.sheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition(
                        type=type, values=[value]),
                format=CellFormat(backgroundColor=clr,
                )))
    
    def create_color(self, r=0.56,g=0.77,b=0.49):
        return Color(red=r,green=g,blue=b)
    
    def add_conditional_format(self, *new_rules):
        rules = get_conditional_format_rules(self.gsc.sheet)
        for rule in new_rules:
            rules.append(rule)
        rules.save()

    def clear_conditional_format(self,):
        rules = get_conditional_format_rules(self.gsc.sheet)
        rules.clear()
        rules.save()