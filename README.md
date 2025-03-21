# ALFRD : Automated Logical FRamework for Dynamic script execution(ALFRD)

This program is written for the [SMILE project](https://smilescience.info) supported by the ERC starting grant, particularly with following purposes in mind:

- Communicate with google spreadsheets and update progress periodically when required.
- Run pipeline based on the spreadsheet progress/requirements.

Contents:
1. [Create API credentials on Google Cloud](#1-create-api-credentials-on-google-cloud)
2. [Installing](#2-installing)
3. [Using ALFRD](#3-using-alfrd)
4. [Attribution](#4-attribution)
5. [Acknowledgement](#5-acknowledgement)

## 1. Create API credentials on Google Cloud


A similar guide is available [here](https://developers.google.com/workspace/guides/create-credentials) or [https://developers.google.com/workspace/guides/create-credentials](https://developers.google.com/workspace/guides/create-credentials)

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

## 2. Installing

- Install using the pip package manager:
  ```bash
  pip install alfrd
  ```
- Alternatively Download [ALFRD](https://github.com/avialxee/alfrd) and unzip / Or 
    ```bash
   git clone https://github.com/avialxee/alfrd
   cd alfrd/
   pip install .
    ```
this should install alfrd and all the dependencies automatically.
    

## 3. Using ALFRD

ALFRD is meant to be used as a tool to create a pipeline/workflow. The pipeline can be visualised as a tabular data e.g in a pandas dataframe table, google spreadsheet etc. For example each column may represent a pipeline step and each row corrosponds to a different dataset. A count of success and failure is kept throughout the code for housekeeping.

### 3.1 ALFRD for Pipeline

Use ALFRD decorators for the pipelines, for:
- *Validator* : using `@validator` decorator on the function which will hold a validation rule i.e function which will be executed on the parameter values before running the pipeline step.
- *Validate Functions* : using `@validate` decorator on the funciton which will be the pipeline step and requires one of the validator to be executed when the pipeline step is called.
- *Register Functions* : using `@register` decorator on the funciton which will be the pipeline step

> Note: If you are using Validators, then define functions in the following order - `@validator` then `@register` and finally `@validate`.

##### Example : Using the ALFRD Decorators
```python 
# pipeline.py

from alfrd.plugins import register, validate, validator

@validator("for general")
def general(params):
"""logic for general params validation"""
    print("general sahab validated!")

@validator("for row operations")
def row_validation(params):
"""logic for another params validation"""
    if "name" in params:
        print("name validated!")
        return True
    else:
        return False

@validate(v=["general", "row_validation"])
@register(desc="prints hello by name")
def hello(name):
    print("hello",name)
```

```bash
$ alfrd init project_name
$ alfrd add path/to/pipeline.py project_name
$ alfrd --help
 Usage: alfrd [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                                              
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                                                                                                                    │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                                                                                                             │
│ --help                        Show this message and exit.                                                                                                                                                                                                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ init   Initialize the project-specific plugin directory.                                                                                                                                                                                                                                                                   │
│ ls     List all available pipeline steps for a project.                                                                                                                                                                                                                                                                    │
│ run    Run a specific pipeline step for a project.                                                                                                                                                                                                                                                                         │
│ add    Add a new plugin to a specific project.                                                                                                                                                                                                                                                                             │
│ rm     Remove a specific project.                                                                                                                                                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

$ alfrd run hello name=Anonymous
hello Anonymous

```

```bash
$ alfrd run --help
                                                                                                                                                                                                                                                                                                                              
 Usage: alfrd run [OPTIONS] STEP_NAME PROJ [PARAMS]...                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                              
 Run a specific pipeline step for a project.                                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                                              
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    step_name      TEXT         [default: None] [required]                                                                                                                                                                                                                                                                │
│ *    proj           TEXT         [default: None] [required]                                                                                                                                                                                                                                                                │
│      params         [PARAMS]...  Key-value pairs of parameters or parameter file path (e.g., id=123 name=Test) [default: None]                                                                                                                                                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                                                                                                                                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


```


##### Example 1 : Initializing and creating instance

```python
from alfrd.lib import GSC, LogFrame
from alfrd.util import timeinmin, read_inputfile

url='https://spreadsheet/link'
worksheet='worksheet-name'

gsc = GSC(url=url, wname=worksheet, key='path/to/json/file')      # default path for key = home/usr/.alfred
df_sheet = gsc.open()
```

##### Example 2: Inititalize the framework

```python
lf = LogFrame(gsc)
lf.primary_colname          =   'FILE_NAME'
```
>The dataframe from the sheet can also be accessed through the instance `lf` using `lf.df_sheet`.

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
> Here the variable `count` and `failed` is used for housekeeping the success/failure of each function call. This can be useful for ensuring minimal API calls, communication to the sheet only when there is a new update.

##### Example 4: using column logic and adding values to the cell on success/failures

Let's say we have a `result` that we need to update to the cell corrosponding to the column `Comment` and row corrosponding to the Serial Number `3`. Where `S.No.` is the column name for serial number.

```python
lf.primary_colname          =   'S.No.'
lf.primary_value            =   '3'
if lf.isvalue(value='True', colname='TSYS') and lf.isval_unique('Project'):
    
    lf.working_col          =   'Comment'                                          # working column
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

`lf.update_sheet` updates the changes to the spreadsheet.

```python
lf.update_sheet(count=count, failed=failed, csvfile='df_sheet.csv')                     # if updating the sheet fails, a copy of the dataframe is saved locally at the csvfile path.

```

>NOTE: The `count` and `failed` parameter corrosponds to a success/fail event on each iteration of update_sheet i.e., if the values of count/fail do not change on the current iteration, the sheet will not be updated and a `skipped` message will appear on the terminal.


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

## 4. Attribution

When using ALFRD, please add a link to this repository in a footnote.

## 5. Acknowledgement

ALFRD was developed within the "Search for Milli-Lenses" (SMILE) project. SMILE has received funding from the European Research Council (ERC) under the HORIZON ERC Grants 2021 programme (grant agreement No. 101040021).