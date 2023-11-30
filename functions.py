import base64, os, json, logging, sys, time, shutil
import variables as var
from subprocess import Popen, PIPE

dir = os.getcwd()
path_git = dir + '/' + var.repo_name
work_dir = dir + '/'

logging.basicConfig(filename='/tmp/terraform_check.log', encoding='utf-8', 
                        level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

validate_path    = os.path.isdir(f'{path_git}')
            
try:
    auth = base64.b64decode(os.environ.get('token')).decode('utf-8')
    logging.info('Environments credentials ok.')
except:
    logging.error('Please check your credentials on github.')
    sys.exit()
    
class git_hub:
    #### Clear directory repo ####
    def clear_directory():
        if validate_path == True:
            shutil.rmtree(path_git)        
            logging.info('Clear diretory successfuly.')
        else:
            logging.error('Error clear diretory') 
            
    #### login GH ####
    def login():
        # using an access token
        try:
            file = open('token.txt', 'w')
            file.write(auth)
            file.close()
            logging.info('Token decode successfully.')
        except:
            logging.error('Token decode unsuccessfully. Please try create environment variable "token"')
            
        if os.system('gh auth login --with-token < token.txt') == 0:         
            logging.info('Login on GH CLI successfully!')
            os.system('rm -f token.txt')
            return 'login_ok'
        else:
            logging.error('Login on GH CLI unsuccessfully, make sure the "token" variable exists. ')
            return 'login_error'
            sys.exit()
        
    #### Create directory to clone ####
    def create_dir():
        result = None
        if not validate_path:             
            result = os.system(f'mkdir {path_git}')
            logging.info("dir create")
            return result
        else:
            result = os.system(f'mkdir -p {path_git}')
            logging.info("dir create")
        return result
    
    #### Clone to repository ####
    def clone_repo():
        result = None
        if git_hub.create_dir() == 0:
            result = os.system(f'git clone https://{auth}@github.com/{var.organization}/{var.repo_name}.git {path_git}  > /dev/null') 
            logging.info('Repository cloned successfully!')
            return result
        else:
            logging.error('The directory to clone the repository does not exist, please check.')
            sys.exit()
        return result
            
    #### commit_new_branch ####
    def commit_branch_fake():
        result = None
        if git_hub.clone_repo() == 0:
            if len(var.repos) >= 1:
                for i in range(len(var.repos)):
                    if os.system(f'git -C {path_git} remote add origin {var.host + var.repos[i]}') == 0:
                        logging.info('Remote repository added successfully.')
                    else:
                        logging.warning('Remote repository not added successfully.')
                        
                    if os.system(f'git -C {path_git} checkout -b {var.branch}  > /dev/null') == 0:
                        logging.info('Branch created successfully.')
                    else:
                        logging.error('Failed - Branch not created, please check.')
                    
                    if os.system(f'git -C {path_git} add .') == 0:
                        logging.info('Commit files added successfully.')             
                    else:                 
                        logging.error('Failed to add commit files, please check.')
                    
                    if  os.system(f'git -C {path_git} commit --allow-empty -m "{var.commit_message}"') == 0:
                        logging.info('Commit completed.')
                    else:
                        logging.error('Failed to commit files, please check.')
                        
                    os.chdir(path_git)
                    
                    if os.system(f'git -C {path_git} push -f --all origin') == 0:
                        logging.info('Push completed.')
                        result = "True"
                        return result
                    else:
                        logging.error('Push failed, please check.')
                        Result = "False"
                        return result
        return result
  
    #### create pr ####
    def create_pr():
        title = "Check terraforms" 
        body = "Check repos terraform"
        command_os = ""
        result = None
        
        if git_hub.commit_branch_fake() ==  "True":
            for i in range(len(var.repos)):
                if os.system(f'gh pr create --repo {var.host + var.repos[i]} --title "{title}" --body "{body}"') == 0:
                    logging.info('Pull request create successfuly.')
                    result = "True"
                    return result   
        else:
            logging.error('Unable to create pull request, please check and try again.')
            result = "False"
            return result
        
        return result
    
    #### comment pr ####
    def run_atlantis(atlantis_command):
        if len(var.atlantis) >= 1:
            for i in range(len(var.repos)):
                os.chdir(path_git)
                pr_data = os.popen('gh pr list --json number').read().strip()
                pr_json = json.loads(pr_data)
                last_pr = pr_json[0]['number']
                os.system(f'gh pr --repo {var.host + var.repos[i]} comment {last_pr} --body "{atlantis_command}"')
        else:
            logging.error('Unable to create comment, please check and try again.')  

    #### read comments ####
    def read_comments():
        try:
            if len(var.atlantis) >= 1:
                for i in range(len(var.repos)):
                    os.chdir(path_git)
                    pr_data = os.popen('gh pr list --json number').read().strip()
                    pr_json = json.loads(pr_data)
                    last_pr = pr_json[0]['number']
                    #os.system(f'gh pr view -R {var.host + var.repos[i]} --comments {last_pr}')
                    comments_data = os.popen(f'gh pr view -R {var.host + var.repos[i]} --comments {last_pr} --json comments').read().strip()
                    comments_data_json = json.loads(comments_data)
                    comment =  'Created in: ' + comments_data_json['comments'][-1]['createdAt'] + ' | Command Run: ' + comments_data_json['comments'][-1]['body']
                    logging.info(comment)
                    logging.info('Comments read successfully.')
            else:
                logging.error('Please check if the repository list exists.')

            return comments_data_json
        
        except:
            logging.error('Please check if the repository list exists.')
    
    #### Close pr ####    
    def close_pr():
        if len(var.repos) >= 1:
            for i in range(len(var.repos)):
                os.chdir(path_git)
                pr_data = os.popen('gh pr list --json number').read().strip()
                pr_json = json.loads(pr_data)
                last_pr = pr_json[0]['number']
                os.system(f'gh pr close -R {var.host + var.repos[i]} {last_pr}')                
                logging.info("Pull request closed successfuly.")
        else:
            logging.error('Unable to closed pull request, please check and try again.')
            
    #### delete branch ####
    def remove_branch():
        if os.system(f'git push -d https://{auth}@github.com/{var.organization}/{var.repo_name}.git {var.branch}') == 0:
            logging.info('Branch deleted success fully.')
        else:
            logging.info('Branch deleted unsuccessfully.')