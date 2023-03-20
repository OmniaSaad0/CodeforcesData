import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from itertools import zip_longest

handles = []
rate = []
maxRate = []
numOfProblems = []
numOfContests = []

def getRate(soup):
    rate = soup.find_all('span')[19].text
    return rate


def getMaxRate(soup):
    maxRate = soup.find_all('span')[20].text
    return maxRate

def getNumOfSolvedProblems(soup):
    problemsNum = soup.find_all('div', {"class": "_UserActivityFrame_counterValue"})[0].text
    return problemsNum

def getSoup(handle):
    url = "https://codeforces.com/profile/"+str(handle)
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    temp = soup.find_all('div', {'class': 'second-level-menu'})
    if len(temp) == 0 :
        return 'nosoup'
    return soup

def getNumOfContests(handle):
    url = "https://codeforces.com/contests/with/"+str(handle)
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "lxml")
    contestTable = soup.find('table', {'class': 'tablesorter user-contests-table'})
    if contestTable is None :
        return '-1'
    contest = contestTable.find('td')
    if contest is None :
        return '0'
    return contest.text


df = pd.read_csv('Dev Handels.csv')
handles = df['codeforces handle'].str.strip().tolist()
for handl in handles :
    soup = getSoup(handl)
    if soup == 'nosoup':
        print(handl)
        continue
    rate.append(getRate(soup))
    maxRate.append(getMaxRate(soup))
    numOfProblems.append(getNumOfSolvedProblems(soup))
    numOfContests.append(getNumOfContests(handl))


df['Rate'] = rate
df['Max Rate'] = maxRate
df['Number Of Solved Problems'] = numOfProblems
df['Number Of Particpeated Rounds'] = numOfContests

df.to_csv("AllDevData.csv" , index = False)


print("Done...")