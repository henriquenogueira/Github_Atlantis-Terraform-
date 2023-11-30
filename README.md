# Terraform Monitoring With MS Teams 
This project was created to monitor repositories in github. In here you can monitor the repository by running the script on Jenkins pipelines.

## Getting Started
Create a pipeline in Jenkins and write the environments variables:

## Environment Variables

To run this project, you will need to add the following environment variables.

`repos` values eg: myorganization/myrepo

`repo_name` values eg: myrepo

`organization` values eg: myorganization

### Prerequisites
Libraries, software and plugins needed to run this project.

```
  pymsteams
```
#### Install pymsteams
```
  pip install pymsteams or pip install -r requirements.txt
```

#### Install GH CLI
```
  apt update && apt install gh
```

## 🔗 Links
[Library link](https://pypi.org/project/pymsteams/)


[GitHub CLI](https://cli.github.com/manual/)

## Usage
Instructions on how to use the project or its features.
```
  python main.py or main.py
```

## Execution logs
You can see the logs in directory on file terraform_check.log.
```
  /tmp/terraform_check.log.
```