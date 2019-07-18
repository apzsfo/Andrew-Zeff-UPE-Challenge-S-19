#!/usr/bin/python

import requests
import json

baseURL =  'http://ec2-34-212-54-152.us-west-2.compute.amazonaws.com'
u = '804994987'
data = {'uid' : u}
headers = {"content-type" : "application/x-www-form-urlencoded"}
r = requests.post(url = baseURL + "/session", data = data, headers = headers)
body = r.json()
token = body['token']

def result(d):
    data = {"action": d}
    r = requests.post(url = baseURL + '/game?token=' + token, data = data, headers = headers)
    move = r.json()
    return move['result']

def solver(i, j, height, width):
    visited[i][j] = True
    #LEFT
    if(j-1 >= 0 and visited[i][j-1] == False):
        move = result("left")
        if(move == -1):
            visited[i][j-1] = True
        if(move == 1):
            return True
        if(move == 0):
            if(solver(i, j-1, height, width)):
                return True
            else:
                result("right")
    #UP
    if(i-1 >= 0 and visited[i-1][j] == False):
        move = result("up")
        if(move == -1):
            visited[i-1][j] = True
        if(move == 1):
            return True
        if(move == 0):
            if(solver(i-1, j, height, width)):
                return True
            else:
                result("down")
    #RIGHT
    if(j+1 < width and visited[i][j+1] == False):
        move = result("right")
        if(move == -1):
            visited[i][j+1] = True
        if(move == 1):
            return True
        if(move == 0):
            if(solver(i, j+1, height, width)):
                return True
            else:
                result("left")

    #DOWN
    if(i+1 < height and visited[i+1][j] == False):
        move = result("down")
        if(move == -1):
            visited[i+1][j] = True
        if(move == 1):
            return True
        if(move == 0):
            if(solver(i+1, j, height, width)):
                return True
            else:
                result("up")
    return False




resp = requests.get(baseURL + '/game?token=' + token)
state = resp.json()

level = 1

while(level <= 5):
    width = state['size'][0]
    height = state['size'][1]
    x = state['cur_loc'][0]
    y = state['cur_loc'][1]
    visited = [[False for j in range(width)] for i in range(height)]
    print(solver(y, x, height, width))
    resp = requests.get(baseURL + '/game?token=' + token)
    state = resp.json()
    if(state['status'] == "GAME_OVER" or state['status'] == "NONE"):
        print("You failed to solve all five mazes")
        break;
    if(state['status'] == "FINISHED"):
        print("SUCCESS")
        break
    if(state['status'] == "PLAYING"):
       print("IN PROGRESS")
    level = level+1
    
