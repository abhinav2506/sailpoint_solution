import json
import requests
import datetime
import re

githubUser=""
githubRepo=""

gitRepo = input("Enter github repo : ")
matchRepoUrl = re.match(r"https://github.com/(.*)/(.*)", gitRepo)
if matchRepoUrl == None:
    print("ERROR :: Incorrect Repo URL provided")
    print("Eg:- https://github.com/abhinav2506/csvserver_solution")
    exit()
else:
    githubUser=matchRepoUrl.group(1)
    githubRepo=matchRepoUrl.group(2)

gitPrType = input("Enter pull request type (open/closed/all) : ")
if gitPrType.lower() not in ['open','closed','all'] :
    print("ERROR :: Incorrect input, accepted input (open/closed/all)")
    exit()

response = requests.get("https://api.github.com/repos/"+githubUser+"/"+githubRepo+"/pulls?state="+gitPrType)
jsonData = json.loads(response.text)


dateNow = datetime.datetime.now()
finalPRList = []

for i in jsonData:
    #print(i['html_url'])
    #print(i['created_at'])
    #print(i['state'])
    match = re.match(r"(.*)-(.*)-(.*)T(.*):(.*):(.*)Z", i['created_at'])
    
    datePR = datetime.datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)), int(match.group(6)))
    timeDiff = dateNow-datePR
    if divmod(timeDiff.total_seconds(), 60)[0] <= 10080 :
        finalPRList.append(i)
        
if len(finalPRList) > 0 :
    toMail = input("Enter mail id to send Report : ")
    if not re.match("^[a-zA-Z0-9][a-zA-Z0-9-_.]+@[a-zA-Z0-9]+\.[a-z]{1,3}$",toMail):
        print("ERROR :: Please enter correct mail id")
        exit()

    print("\n\n============================== Email ==============================\n\n")
    print("From : report@company.com")
    print("To : "+toMail)
    print("Subject:- "+gitPrType.upper()+" pull requests of repo "+gitRepo+" within 1 week\n\n")
    print("Body:- ")
    print("\nList of pull request:-")
    for i in finalPRList:
        print("\t * "+i['html_url'])
    print("\n\n===================================================================")
else :
    print("No "+gitPrType.upper()+" Pull request within 1 week")