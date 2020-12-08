import random
import json
file = {}
with open('settings.json', 'r', encoding='utf-8') as read_file:
    file = dict(json.load(read_file))
glx = file['x']
if glx<10:
    glx = 9
gly = file['y']
if gly<10:
    gly = 9
def gen():
    global file, glx, gly
    lis = {}
    bomd_cs = []
    for i in range(glx*gly-file["bombs"]):
        bomd_cs.append(0)
    for i in range(file["bombs"]):            
        bomd_cs.append('B')



    for i in range(glx):
        for j in range(gly):
            alph =  random.choice(bomd_cs)
            lis[(i, j)] = alph
            bomd_cs.remove(alph)

    for i in list(lis.keys()):
        if lis[i] == 'B':
            total = 0
            for n in [-1, 0, 1]:
                for m in  [-1, 0, 1]:
                    a = i[0]+n
                    b = i[1]+m
                    if a in range (glx) and b in range (gly):
                        if lis[(a, b)]  != 'B':
                            lis[(a, b)] += 1

    return lis


