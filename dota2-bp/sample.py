import dota2bp
import pandas as pd
import numpy as np

heroList = dota2bp.getHeroList('data\heroes.json')

def getHeroNameById(id):
  return heroList[id]['chinese_name']


def getHeroIdByName(name):
  for hero in heroList:
    if hero['chinese_name'] == name:
      return hero['id']
  return 'unknown'

A = dota2bp.load('matrix_A.pkl')
B = dota2bp.load('matrix_B.pkl')

pickList_A = []
pickList_B = []
banList = []

# 1 means 'team A round', 2 means 'team B round'
AorB = [1,2,1,2,1,2,2,1,2,1,2,1,2,1,2,1,2,1,1,2]
# 1 means 'ban', 2 means 'pick'
BorP = [1,1,1,1,2,2,2,2,1,1,1,1,2,2,2,2,1,1,2,2]

for i in range(20):
  print('round ', i + 1)
  if AorB[i] == 1 and BorP[i] == 1:
    a_ban = input('team A ban: ')
    while getHeroIdByName(a_ban) == 'unknown':
      a_ban = input('Unknown hero, please input again: ')
    banList.append(getHeroIdByName(a_ban) - 1)
    print('team A banned: ', a_ban)
  elif AorB[i] == 1 and BorP[i] == 2:
    a_pick = input('team A pick: ')
    while getHeroIdByName(a_pick) == 'unknown':
      a_pick = input('Unknown hero, please input again: ')
    pickList_A.append(getHeroIdByName(a_pick) - 1)
    print('team A picked: ', a_pick)
  elif AorB[i] == 2 and BorP[i] == 1:
    ban = dota2bp.getBanAdvise(A, B, pickList_A, pickList_B, banList)
    banList.append(ban)
    print('team B banned: ', getHeroNameById(ban))
  elif AorB[i] == 2 and BorP[i] == 2:
    pick = dota2bp.getPickAdvise(A, B, pickList_A, pickList_B, banList)
    pickList_B.append(pick)
    print('team B picked: ', getHeroNameById(pick))


print("result:")
print("team A picked:")
for ele in pickList_A:
  print(getHeroNameById(ele), ' ')
print("team B picked")
for ele in pickList_B:
  print(getHeroNameById(ele), ' ')