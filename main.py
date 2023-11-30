#!/usr/bin/env python
import functions as f
import pymsteams

# You must create the connectorcard object with the Microsoft Webhook URL
send_notifications = pymsteams.connectorcard(f.var.teams)

class main:
    #### check gh are installed ####
    def check_gh():
        if f.os.system('gh --version') == 0:
            f.logging.info('GH CLI Working!')
        else:
            f.logging.error('GH CLI not installed, please install and try again.')
            f.sys.exit()
            
    def run():
        ##### login github ####    
        if f.git_hub.login() == "login_ok":
            f.git_hub.login()

        elif f.git_hub.login() == "login_error":     
            f.sys.exit()
        
        ##### Execute functions on github ####    
        def execute_pr():
            if f.git_hub.create_pr() == "True":
                for i in range(len(f.var.atlantis)):
                    f.git_hub.run_atlantis(f'atlantis plan -w {f.var.atlantis[i]}')
                    pr_data = f.os.popen('gh pr list --json number').read().strip()
                    pr_json = f.json.loads(pr_data)
                    last_pr = pr_json[0]['number']
                    while f.git_hub.read_comments()['comments'][-1]['body'][0:8] == 'atlantis':
                        #f.git_hub.read_comments()
                        f.logging.info('Wait atlantis finish process...')
                        f.time.sleep(5)
                        if f.git_hub.read_comments()['comments'][-1]['body'][0:8]  != 'atlantis':
                            # Add text to the message.
                            send_notifications.text(f'Pull request : {f.var.host + f.var.repos[0]}/pull/{last_pr} "\n" \
                                                    Created in: {f.git_hub.read_comments()["comments"][-1]["createdAt"]} "\n" \
                                                    {f.git_hub.read_comments()["comments"][-1]["body"]}')
                            # send the message.
                            send_notifications.send()
                            f.logging.info('Notification sent to teams channel ec-oklahoma -> develop.')
                f.git_hub.close_pr()
                f.git_hub.remove_branch()
            else:
                f.logging.error('Altantis run error, please check.')           
        
        main.check_gh()
        f.git_hub.clear_directory()
        execute_pr()
        
if __name__ == '__main__':
    try:
        f.logging.info('Running...')
        main.run()
    except:
        f.logging.error('Error when executing.')      
