#!/usr/local/env python
# version 0.1-release.20160315
import os, json, math, random
os.chdir(os.path.dirname(__file__))
my_file = open('./data.json')
data = json.loads(my_file.read())
data = data['data']


def distance(x, y):
    x1 = x - 9
    y1 = y + 1
    return math.sqrt(x1 * x1 + y1 * y1)


def comp(a):
    return distance(a['x'], a['y'])

data.sort(key=comp)
students = {}
for seat in data:
    for name in seat['best']:
        if name in students:
            seat['best'].remove(name)
            seat['soso'].append(name)
        else:
            students[name] = []
        students[name].append({'x': seat['x'], 'y': seat['y']})
    for name in seat['soso']:
        if name not in students:
            seat['best'].append(name)
            seat['soso'].remove(name)
            students[name] = []
        students[name].append({'x': seat['x'], 'y': seat['y']})
for pos in students.values():
    pos.sort(key=comp)
    for p1 in pos:
        for p2 in pos:
            if p1 is p2:
                continue
            if p1['x'] == p2['x'] and p1['y'] == p2['y']:
                pos.remove(p2)

result = []
for seat in data:
    def pos_in_result(x, y):
        for r in result:
            if r['x'] == x and r['y'] == y:
                return True
        return False
    stus = seat['best']
    if len(stus) == 0:
        continue
    n = random.randrange(len(stus))
    result.append({'x': seat['x'], 'y': seat['y'], 'name': stus[n]})
    for s in stus:
        if s is stus[n]:
            continue
        flag = True
        for pos in students[s]:

            if pos_in_result(pos['x'], pos['y']):
                continue
            # noinspection PyRedeclaration
            flag = False

            def get_item_from_data(x, y):
                for d in data:
                    if d['x'] == x and d['y'] == y:
                        return d
                return None
            p = get_item_from_data(pos['x'], pos['y'])
            p['best'].append(s)
            break
        if flag:
            for d in data:
                if pos_in_result(d['x'], d['y']):
                    continue
                d.append(s)
                break

f = open('./result.py', mode='w')
print('# coding=utf-8', file=f)
print('result = %s' % str(result), file=f)
