import argparse, ast, sys, json
from pathlib import Path
import importlib


c={"x":"\033[0m","g":"\033[32m", "r":"\033[31m", "b":"\033[34m","c":"\033[36m","w":"\033[0m", "y":"\033[33m"}

alfrddir = str(Path.home())+'/.alfrd/'


def get_functionnames(tree=None, modulfile=None, match='', classes=True):
    
    if modulfile is not None: 
        with open(modulfile) as f:
            tree=ast.parse(f.read())
                
    functiondefs=[]
    for elem in tree.body:
        if classes:
            if isinstance(elem, ast.ClassDef):
                for child in elem.body:
                    if isinstance(child, ast.FunctionDef):
                        child.parent = elem
                        if match in child.name:functiondefs.append(child.name)
        elif isinstance(elem,ast.FunctionDef): 
            if match in elem.name:
                functiondefs.append(elem.name)
                params = [arg.arg for arg in elem.args.args]
                return params

parser = argparse.ArgumentParser('alfrd', description="""
Automated Logical FRamework for Dynamic script execution(ALFRD)
""", 
formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)

parser.add_argument('input_file', help='Give the input file path.', nargs='*')
parser.add_argument('-s','--setup', help="to setup path/to/script.py", required=False, action="store_true")
parser.add_argument('-m','--main-method', help="name of the main()", required=False)




def cli():

    scriptdefault                      =   f'{alfrddir}/default.json'
    args                            =   parser.parse_known_args()[0]
    
    if args.setup:
        Path(scriptdefault).parent.mkdir(parents=True, exist_ok=True)
        config_dict = args.__dict__
        

        if args.main_method:
            params = get_functionnames(modulfile=args.input_file[0], match=args.main_method,classes=False)
            config_dict['p'] = {}
            print(f"Enter for default values else pass the default values for each parameters of {args.main_method}")
            for p in params:
                if not 'setup' in p.lower():
                    p_value = input(f"{p}=")
                    if p_value:
                        try:
                            p_value = float(p_value)
                        except:
                            try:
                                p_value = int(p_value)
                            except:
                                p_value = str(p_value)
                        config_dict['p'][p]= p_value
            
        with open(str(scriptdefault), 'w') as sf: 
            json.dump(config_dict, sf)
    else:
        with open(scriptdefault, 'r') as sf:
            df_params = json.load(sf)
        args.main_method = df_params["main_method"]
        args.input_file = df_params["input_file"]
        params_dict = df_params['p']
        
            
        # addmsg = f"""
        # if __name__ == '__main__':
        #       import argparse
        #       {args.main_method}(**{params_dict})
        #       parser = argparse.
        #       """
        sys.path.insert(0, str(Path(args.input_file[0]).parent))
        mod = importlib.import_module(f"{str(Path(args.input_file[0]).stem)}")
        working_cols = eval(f"mod.{args.main_method}(**{params_dict}, setup=True)")
        cols=parser.add_argument_group('cols')
        for i, parg in enumerate(working_cols):
            cols.add_argument(f'-c{i}',f"--{parg}")
        parser.add_argument('-h',action='help')
        args                            =   parser.parse_args()
        
        # addmsg += f"argparse.ArgumentParser('alfrd',"
        # print(eval(f"{mod}.{args.main_method}"))
        # print(eval(f"{mod}.{args.main_method}")(setup=True))
    # elif Path(scriptfile).exists():
    #     parser.add_argument()
        
    

