# ALFRD : Automated Logical FRamework for executing scripts Dynamically

This program is written for the [SMILE project](smilescience.info) supported by the ERC starting grant, particularly with following purposes in mind:

- Communicate with google spreadsheets and update progress periodically when required.
- Run pipeline based on the spreadsheet progress/requirements.


### 1. Create API credentials on Google Cloud


A similar guide is available [here](https://www.cybrosys.com/blog/how-to-use-gspread-python-api)

NOTE: In order to successfully create a google console project a billing detail is usually required. But the sheets API service is available for free, refer [here](https://developers.google.com/sheets/api/limits)

- step 1:
  Go to https://console.cloud.google.com/

- step 2: 
	click on the drop-down to create a new project 
		- can choose organization or leave on default

- step 3
  Search in the top bar (or press / ) and type : "Google sheets api"
  
- step 4
  In the search results - under Marketplace select the first result which should be the same : Google sheets api
  
- step 5
  Enable the service In the product details page 
  
- step 6
  Now select create credentials > Application Data
  
- step 7
  Create an account name
  Select create and continue
  
- step 8
  Search and select "Editor" in role > Continue
  
- step 9
  Skip next optional step
  Select Done
  
- step 10
  The Credentials are successfully created
  Select "Credentials" on the left menu
  
- step 11
  select/edit account that was just created
  also copy the email address that is shown
  
- step 12
  Select keys tab > Add keys > Create New Keys > JSON > save
  
- step 13
  Go to the Google spreadsheet and "share" the sheet to the email address that was copied, as Editor.

### 2. Installing

- Download [ALFRD](https://github.com/avialxee/alfrd) and unzip / Or 
   `git clone https://github.com/avialxee/alfrd`
   
- install alfrd
    ```
   cd alfrd/
   pip install .
    ```
    this should install alfrd and all the dependencies automatically.
    

### 3. Using ALFRD

##### Example 1 : Initializing and creating instance

```python
from alfrd.lib import GSC, LogFrame
from alfrd.util import timeinmin, read_inputfile

url='https://spreadsheet/link'
worksheet='worksheet-name'

gsc = GSC(url=url, wname=worksheet, key='path/to/json/file')      # default path for key = home/usr/.alfred
_ = gsc.open()
```

##### Example 2: Inititalize the framework

```python
lf = LogFrame(gsc)
lf.primary_colname          =   'FILE_NAME'
```

##### Example 3: Run - Iterate for each row

```python
from pathlib import Path
import time, subprocess
import glob

count,failed=0,0
allfiles=[]
folder_for_fits ='path/to/allfits'

allfiles.extend(glob.glob(f"{folder_for_fits}*/*fits"))

for fitsfile in allfiles:
    fitsfile_name = Path(fitsfile).name
    lf.primary_value            =   fitsfile_name
```

##### Example 4: using column logic and adding values on success/failures

```python
if lf.isvalue(value='True', colname='TSYS') and lf.isval_unique('Project'):
    
    lf.working_col          =   'Comment1'                                          # working column
    print(lf.get_value())

    result                  =   'test'
    if result :
        count               =   lf.put_value(result, count=count)                   
    else:
        failed              =   lf.put_value('failed: logfile_path', count=failed)
    
    print(lf.get_value())
```

##### Example 5: Script execution

```python
def run_picard(cmd):
    t0 = time.time()
    subprocess.run(cmd)
    t1 = time.time()
    td = timeinmin(t1-t0)
    return td

def scripted_picard_1(wd_ifolder, count, failed, col='fits to ms'):
    """
    converts fitsfile to ms file; checks if conversion was successful; skips if file exists; logs in the spreadsheet;
    """
    td=0
    cmd=["picard",'-n','10',"-l","e",'--input',wd_ifolder]
       
    params, files, input_folder = read_inputfile(wd_ifolder, "observation.inp")
    
    if not Path(f"{wd_ifolder}").exists():
        print('input folder missing..')
    elif not Path(f"{wd_ifolder}/../{params['ms_name']}").exists():
        td          =   run_picard(cmd)
        count       =   lf.put_value(colname=col, value=td, count=count)
    elif Path(f"{wd_ifolder}/../{params['ms_name']}").exists():
        print('skipped')

    if not Path(f"{wd_ifolder}/../{params['ms_name']}").exists():
        count-=1
        failed      =   lf.put_value(colname=col, value='failed',count=failed)
    return td, count, failed

if lf.isvalue(value='True', colname='TSYS') and lf.isval_unique('Project'):
    lf.working_col          =   'Comment1'
    ttaken, count, failed   =   scripted_picard_1(wd_ifolder='path/to/wd/input_template', count=count, failed=failed )

print(lf.get_value(colname='fits to ms'))
```

##### Example 6: Update the sheet

```python
lf.update_sheet(count=count, failed=failed, csvfile='df_sheet.csv')                     # if updating the sheet fails, a copy of the dataframe is saved locally at the csvfile path.

```


##### Example 7: Conditional Formatting
need to run only once.

```python
r1 = lf.create_rule(range='G2:G105', type='TEXT_CONTAINS' ,value='False', c='r')               # check if TSYS == False --> background color = red
r2 = lf.create_rule(range='G2:G105', type="TEXT_CONTAINS", value='True', custom_clr=lf.create_color(0.56, 0.77, 0.49))
r3 = lf.create_conditional_format(range='F2:F105', c='g', valtype='timeinmin')              # check if value in XXmYYs format --> background color = green

r4 = lf.create_conditional_format(range='F2:F105', c='r', valtype='fail')                   # check if value contains fail --> background color = red
r4 = lf.create_rule(range='F2:F105', type='TEXT_CONTAINS', c='r', value='fail')                # similar to above
print(r1,r2,r3,r4)
lf.add_conditional_format(r1, r2, r3, r4)
```

### Attribution

When using ALFRD, please add a link to this repository in a footnote.

### Acknowledgement

ALFRD was developed within the "Search for Milli-Lenses" (SMILE) project. SMILE has received funding from the European Research Council (ERC) under the HORIZON ERC Grants 2021 programme (grant agreement No. 101040021).