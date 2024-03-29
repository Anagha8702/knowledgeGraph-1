from tracemalloc import start
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import os, pickle
import csv
import networkx as nx

global loading
loading = 0

def load():
    global g
    g = nx.MultiGraph()
    path = os.path.dirname(os.path.realpath(__file__)) + "/Graph1.txt"
    g = pickle.load(open(path,'rb'))

def products(types,categories,borders,colors):
    global g
    data=[0,[],0]
    for type in types:
        for product in g[type].keys():
            names=product.split('*')
            for item4 in categories:
                if names[1]==item4:
                    for item5 in borders:
                        if names[2]==item5:
                            for item6 in colors:
                                if names[3]==item6:
                                    temp={product : g.nodes[product]['Stock']}
                                    data[0]+=1
                                    data[1].append(temp)
                                    data[2]+= g.nodes[product]['Stock']

    return data

def transactions(months, centres, ratings, wids):
    global g
    data = [0, []]
    if wids:
        for wid in wids:
            for pdt in g[wid].keys():
                for index in g[wid][pdt].keys():
                    transaction = g[wid][pdt][index].copy()
                    if transaction['month'] in months and transaction['centre'] in centres and transaction['rating'] in ratings:
                        transaction['pdt'] = pdt
                        data[1].append(transaction)
                        data[0] += 1

    else:
        for mon in months:
            print(mon)
            for pdt in g[mon].keys():
                for index in g[mon][pdt].keys():
                    transaction = g[mon][pdt][index].copy()
                    if transaction['centre'] in centres and transaction['rating'] in ratings:
                        transaction['pdt'] = pdt
                        data[1].append(transaction)
                        data[0] += 1
    return data

def index(request):
  global loading
  if loading == 0:
      load()
      loading += 1
  formData = {
          'types': ["Accessories", "Art-silk", "Bagru", "Banarasi", "Bhagalpuri", "Chanderi-cotton", "Cotton-linen", "Cotton-tant", "Cotton-voile"],
          'categories': ["AC Blanket(DOHAR)", "Beads", "Bedsheet", "Bermuda", "Bluse", "Chiffon", "Crochet Lace","Cutting Roll", "Fabric", "Fusing", "Girls-Womens Suit", "Shorts"],
          'borders': ["Checks", "Floral", "Golden-Zari", "Lines"],
          'colors': ["Blue", "Red", "Orange", "Violet", "Green", "Yellow", "Indigo"],
          'months': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
          'centres': ["Bangalore", "Hyderabad", "Mumbai"],
          'ratings': ["1s", "2s", "3s", "4s", "5s"]
      }

  if request.method == "POST":
        if request.POST.get('switch') == "product":
            types = request.POST.getlist('type');
            if not types or not types[0]:
                types = formData['types']
            
            categories = request.POST.getlist('category');
            if not categories or not categories[0]:
                categories = formData['categories']
            
            colors = request.POST.getlist('color');
            if not colors or not colors[0]:
                colors = formData['colors']
            
            borders = request.POST.getlist('border');
            if not borders or not borders[0]:
                borders = formData['borders']

            data = products(types, categories, borders, colors)
            pdts =[]
            st = []
            for d in data[1]:
                pdts.append(list(d.keys())[0])
                st.append(int(list(d.values())[0]))

            return render(request, 'first.html', {
                'products': data[0], 
                'table1': data[1] , 
                'tot': data[2],
                'formData': formData,
                'pdts': pdts,
                'st': st 
                }) 
    
        else: 
            months = request.POST.getlist('month')
            if not months or not months[0]:        
                months = formData['months']

            centres = request.POST.getlist('centre')
            if not centres or not centres[0]:
                centres = formData['centres']

            ratings = request.POST.getlist('rating')
            if not ratings or not ratings[0]:
                ratings = formData['ratings']

            wids = request.POST.get('wids')
            if wids:
                wids = wids.split(',')
            else:
                wids = []
            # print(months, centres, ratings, wids)
            data = transactions(months, centres, ratings, wids)
            chartMonth = []
            Wids = []
            top={}
            top_wid = {}
            top_pdt = {}
            l1 = l2 = l3 = l4 = []
            if wids:
                for wid in wids:
                    Wids.append(int(wid))
                    chart = [0,0,0,0,0,0,0,0,0,0,0,0]
                    for tran in data[1]:
                        if(tran['w_id'] == wid):
                            m = tran['month']
                            if m == "January":
                                chart[0] += int(tran['quantity'])
                            elif m == "February":
                                chart[1] += int(tran['quantity'])
                            elif m == "March":
                                chart[2] += int(tran['quantity'])
                            elif m == "April":
                                chart[3] += int(tran['quantity'])
                            elif m == "May":
                                chart[4] += int(tran['quantity'])
                            elif m == "June":
                                chart[5] += int(tran['quantity'])
                            elif m == "July":
                                chart[6] += int(tran['quantity'])
                            elif m == "August":
                                chart[7] += int(tran['quantity'])
                            elif m == "September":
                                chart[8] += int(tran['quantity'])
                            elif m == "October":
                                chart[9] += int(tran['quantity'])
                            elif m == "November":
                                chart[10] += int(tran['quantity'])
                            elif m == "December":
                                chart[11] += int(tran['quantity'])
                    chartMonth.append(chart);                
            else:
                for tran in data[1]:
                    try:
                        top_wid[int(tran['w_id'])] += int(tran['quantity'])
                    except:
                        top_wid[int(tran['w_id'])] = int(tran['quantity'])
                    try:
                        top_pdt[tran['pdt']] += int(tran['quantity'])
                    except:
                        top_pdt[tran['pdt']] = int(tran['quantity'])

                top_wid = {k: v for k, v in sorted(top_wid.items(), key=lambda item: item[1], reverse=True)}
                top_pdt = {k: v for k, v in sorted(top_pdt.items(), key=lambda item: item[1], reverse=True)}
                l1 =  (list(top_wid.keys()))[:10]
                l2 =  (list(top_wid.values()))[:10]
                l3 =  (list(top_pdt.keys()))[:10]
                l4 =  (list(top_pdt.values()))[:10]
                top['wids'] =  zip(l1, l2) 
                top['pdts'] =  zip(l3, l4)

            return render(request, 'first.html', {
                'count': data[0], 
                'table': data[1] , 
                'formData': formData, 
                'chartMonth': chartMonth, 
                'wids': Wids, 
                'top': top,
                'topWid': l1,
                'qtWid': l2,
                'topPdt': l3,
                'qtPdt': l4,
                }) 

  else:
        return render(request, 'first.html', {'count': 0, 'table': "" , 'formData': formData}) 



