import functions as f

#### py variables ####
host  = "https://github.com/"
branch = "atlantis"
atlantis = ["workspace atlantis"]
commit_message = "custom message"
teams = "teams webhook"

#### os environs ####
repos = [f.os.environ.get('repos')]
repo_name = f.os.environ.get('repo_name')
organization = f.os.environ.get('organization')