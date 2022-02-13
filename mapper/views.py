import json
import pandas as pd

from mapper.models import *
from itertools import islice
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 初始界面中美GDP (china1、foreign1)
gdps = GDP.objects.values()
country_list = []
gdp_list = []
for gdp in gdps:
    country_list.append(gdp['country'])
    country_gdp = []
    for name, value in islice(gdp.items(), 2, None):
        year_gdp = [name[-4:], value]
        country_gdp.append(year_gdp)
    gdp_list.append(country_gdp)

# 初始界面EPU (china3、foreign3)
epus = EPU.objects.values()
epus_df = pd.DataFrame(list(epus))
epu_country = epus_df.columns.tolist()[3:]
epu_list = []
for country in epu_country:
    country_epu = []
    for epu in epus:
        if epu[country]:
            country_epu.append([epu['year'] + "." + epu['month'], epu[country]])
        else:
            country_epu.append(0)
    epu_list.append(country_epu)

# 初始界面中美贸易 (china2、foreign2)
relations = RELATION.objects.values()
relations_df = pd.DataFrame(list(relations))
relations_foreign = RELATION_FOREIGN.objects.values()
relations_foreign_df = pd.DataFrame(list(relations_foreign))

export_total = relations_df["export_total"].tolist()
import_total = relations_df["import_total"].tolist()
relations_df.drop(["id", "time", "export_total", "import_total"], axis=1, inplace=True)
relations_foreign_df.drop(["id", "time"], axis=1, inplace=True)

relation_country = ["澳大利亚", "巴西", "法国", "德国", "印度", "意大利", "日本", "韩国", "荷兰", "俄罗斯", "美国", "英国"]
relation_list = []
relation_foreign_list = []
for i in range(len(relation_country) * 2):
    if i % 2 == 1:
        continue
    country_export = relations_df.iloc[:, i].tolist()
    country_import = relations_df.iloc[:, i + 1].tolist()
    foreign_total_export = relations_foreign_df.iloc[:, i].tolist()
    foreign_total_import = relations_foreign_df.iloc[:, i + 1].tolist()
    china_export, china_import, foreign_export, foreign_import = [], [], [], []
    for j in range(len(country_export)):
        china_export.append(country_export[j] / export_total[j] * 100)
        china_import.append(country_import[j] / import_total[j] * 100)
        foreign_export.append(country_import[j] / foreign_total_export[j] * 100)
        foreign_import.append(country_export[j] / foreign_total_import[j] * 100)

    china_foreign = [china_export, china_import]
    foreign_china = [foreign_export, foreign_import]
    relation_list.append(china_foreign)
    relation_foreign_list.append(foreign_china)

tos = TO.objects.values()
tos_df = pd.DataFrame(list(tos))
froms = FROM.objects.values()
froms_df = pd.DataFrame(list(froms))

to_total = tos_df["to_total"].tolist()
from_total = froms_df["from_total"].tolist()
tos_df.drop(["id", "time", "to_total"], axis=1, inplace=True)
froms_df.drop(["id", "time", "from_total"], axis=1, inplace=True)
china_to_from, foreign_from_to = [], []
for i in range(len(relation_country)):
    gdp_china = gdp_list[1]
    index = country_list.index(relation_country[i])
    gdp_i = gdp_list[index]
    china_to = tos_df.iloc[:, i].tolist()
    china_from = froms_df.iloc[:, i].tolist()
    china_to_rate, china_from_rate, foreign_to_rate, foreign_from_rate = [], [], [], []
    for j in range(len(china_to)):
        china_to_rate.append(china_to[j] / gdp_china[j][1] * 100)
        china_from_rate.append(china_from[j] / gdp_china[j][1] * 100)
        foreign_to_rate.append(china_from[j] / gdp_i[j][1] * 100)
        foreign_from_rate.append(china_to[j] / gdp_i[j][1] * 100)

    china_foreign = [china_to_rate, china_from_rate]
    foreign_china = [foreign_to_rate, foreign_from_rate]
    china_to_from.append(china_foreign)
    foreign_from_to.append(foreign_china)

# 对外援助
chn = pd.DataFrame(list(AID_CHN.objects.all().values('recipient', 'year', 'value')))
us = pd.DataFrame(list(AID_US.objects.all().values('recipient', 'year', 'value')))
aid_chn, aid_us, aid_both = [], [], []
year_chn, year_us, year_both = [], [], []
for year in range(2000, 2015):
    year_chn.append(str(year))
    year_aid = []
    aid = chn[chn['year'] == year]
    for i in range(0, len(aid)):
        data = {
            "name": aid.iloc[i]['recipient'],
            "value": aid.iloc[i]['value']
        }
        year_aid.append(data)
    aid_chn.append(year_aid)

for year in range(2005, 2020):
    year_us.append(str(year))
    year_aid = []
    aid = us[us['year'] == year]
    for i in range(0, len(aid)):
        data = {
            "name": aid.iloc[i]['recipient'],
            "value": aid.iloc[i]['value']
        }
        year_aid.append(data)
    aid_us.append(year_aid)

for year in range(2005, 2015):
    year_both.append(str(year))
    year_aid = []
    aid1 = chn[chn['year'] == year]
    aid2 = us[us['year'] == year]
    s = pd.merge(aid1, aid2, how='inner', on='recipient')
    for i in range(0, len(s)):
        data = {
            "name": s.iloc[i]['recipient'],
            "value": s.iloc[i]['value_x'] + s.iloc[i]['value_y']
        }
        aid1 = aid1.drop(aid1[aid1['recipient'] == s.iloc[i]['recipient']].index)
        aid2 = aid2.drop(aid2[aid2['recipient'] == s.iloc[i]['recipient']].index)
        year_aid.append(data)
    for i in range(0, len(aid1)):
        data = {
            "name": aid1.iloc[i]['recipient'],
            "value": aid1.iloc[i]['value']
        }
        year_aid.append(data)
    for i in range(0, len(aid2)):
        data = {
            "name": aid2.iloc[i]['recipient'],
            "value": aid2.iloc[i]['value']
        }
        year_aid.append(data)
    aid_both.append(year_aid)

@csrf_exempt
def home(request):
    send_dict = {
        'country_list': country_list,
        'GDP_list': gdp_list,
        'EPU_country': epu_country,
        'EPU_list': epu_list,
        'relation_country': relation_country,
        "relation_list": relation_list,
        "relation_foreign_list": relation_foreign_list
    }
    return render(request, "Map0.html", send_dict)

def map1(request):
    send_dict = {
        'country_list': country_list,
        'GDP_list': gdp_list,
        'EPU_country': epu_country,
        'EPU_list': epu_list,
        'relation_country': relation_country,
        "relation_list": relation_list,
        "relation_foreign_list": relation_foreign_list
    }
    return render(request, "Map1.html", send_dict)

def map2(request):
    send_dict = {
        'country_list': country_list,
        'GDP_list': gdp_list,
        'EPU_country': epu_country,
        'EPU_list': epu_list,
        'relation_country': relation_country,
        "relation_list": relation_list,
        "relation_foreign_list": relation_foreign_list
    }
    return render(request, "Map2.html", send_dict)

def map3D(request):
    send_dict = {
        'country_list': country_list,
        'GDP_list': gdp_list,
        'EPU_country': epu_country,
        'EPU_list': epu_list,
        'relation_country': relation_country,
        "relation_list": relation_list,
        "relation_foreign_list": relation_foreign_list
    }
    return render(request, "Map3D.html", send_dict)

def aid(request):
    send_dict = {
        'AID_chn': aid_chn
    }
    return render(request, "Rotation_CHN_stock.html", send_dict)

def select_aid(request):
    aid_type = request.POST.get('type', None)[:3]
    if aid_type == 'CHN':
        aid_list = aid_chn
        year_list = year_chn
    elif aid_type == 'US':
        aid_list = aid_us
        year_list = year_us
    else:
        aid_list = aid_both
        year_list = year_both
    send_dict = {
        'AID': aid_list,
        'year_list': year_list
    }
    return HttpResponse(json.dumps(send_dict))

def select_Country_with_type(request):
    ID = request.POST.get('id', None)
    if ID == '0':
        send_dict = {
            'country': "",
            'china_data': "",
            'foreign_data': "",
            'error': "没有当前国家的数据！"
        }
        return HttpResponse(json.dumps(send_dict))

    data_type = request.POST.get('type', None)
    if data_type == "GDP(亿美元)":
        china_data = GDP.objects.filter(id=2).values()[0]
        foreign_data = GDP.objects.filter(id=ID).values()[0]
    elif data_type == "GDP增长率(%)":
        china_data = GDPR.objects.filter(id=2).values()[0]
        foreign_data = GDPR.objects.filter(id=ID).values()[0]
    elif data_type == "人均GDP(美元)":
        china_data = GDPP.objects.filter(id=2).values()[0]
        foreign_data = GDPP.objects.filter(id=ID).values()[0]
    elif data_type == "总投资占比(%)":
        china_data = INVEST.objects.filter(id=2).values()[0]
        foreign_data = INVEST.objects.filter(id=ID).values()[0]
    elif data_type == "通货膨胀率(%)":
        china_data = INFLATION.objects.filter(id=2).values()[0]
        foreign_data = INFLATION.objects.filter(id=ID).values()[0]
    elif data_type == "货物和服务进口量(%)":
        china_data = IMPORT.objects.filter(id=2).values()[0]
        foreign_data = IMPORT.objects.filter(id=ID).values()[0]
    elif data_type == "货物和服务出口量(%)":
        china_data = EXPORT.objects.filter(id=2).values()[0]
        foreign_data = EXPORT.objects.filter(id=ID).values()[0]
    elif data_type == "失业率(%)":
        china_data = UNEM.objects.filter(id=2).values()[0]
        foreign_data = UNEM.objects.filter(id=ID).values()[0]
    elif data_type == "人口(百万)":
        china_data = POPU.objects.filter(id=2).values()[0]
        foreign_data = POPU.objects.filter(id=ID).values()[0]
    elif data_type == "政府收入占比(%)":
        china_data = REVENUE.objects.filter(id=2).values()[0]
        foreign_data = REVENUE.objects.filter(id=ID).values()[0]
    else:
        china_data = COST.objects.filter(id=2).values()[0]
        foreign_data = COST.objects.filter(id=ID).values()[0]

    china, foreign = [], []
    for name, value in islice(china_data.items(), 2, None):
        year_data = [name[-4:], value]
        china.append(year_data)
    for name, value in islice(foreign_data.items(), 2, None):
        year_data = [name[-4:], value]
        foreign.append(year_data)

    send_dict = {
        'country': foreign_data['country'],
        'china_data': china,
        'foreign_data': foreign,
        'error': ""
    }
    return HttpResponse(json.dumps(send_dict))

def select_Country_with_relation(request):
    relation_name = request.POST.get('name', None)
    print(relation_name)
    if relation_name not in relation_country:
        send_dict = {
            'china_data': "",
            'foreign_data': "",
            'error': "没有当前国家的数据！"
        }
        return HttpResponse(json.dumps(send_dict))
    ID = relation_country.index(relation_name)
    data_type = request.POST.get('relation', None)

    if data_type == "对目标国出口额占总出口额比重(%)":
        china_data = relation_list[ID][0]
        foreign_data = relation_foreign_list[ID][0]
    elif data_type == "对目标国进口额占总进口额比重(%)":
        china_data = relation_list[ID][1]
        foreign_data = relation_foreign_list[ID][1]
    elif data_type == "对目标国直接投资占GDP比重(%)":
        china_data = china_to_from[ID][0]
        foreign_data = foreign_from_to[ID][0]
    else:
        china_data = china_to_from[ID][1]
        foreign_data = foreign_from_to[ID][1]

    send_dict = {
        'china_data': china_data,
        'foreign_data': foreign_data,
        'error': ""
    }
    return HttpResponse(json.dumps(send_dict))

def select_Country(request):
    ID = request.POST.get('id', None)
    if ID == '0':
        send_dict = {
            'country': "",
            'china_data': "",
            'foreign_data': "",
            'foreign_epu': "",
            'error': "没有当前国家的数据！"
        }
        return HttpResponse(json.dumps(send_dict))

    china_data = GDP.objects.filter(id=2).values()[0]
    foreign_data = GDP.objects.filter(id=ID).values()[0]

    china, foreign = [], []
    for name, value in islice(china_data.items(), 2, None):
        year_data = [name[-4:], value]
        china.append(year_data)
    for name, value in islice(foreign_data.items(), 2, None):
        year_data = [name[-4:], value]
        foreign.append(year_data)

    send_dict = {
        'country': foreign_data['country'],
        'china_data': china,
        'foreign_data': foreign,
        'foreign_epu': 'epu_list[]',
        'error': ""
    }
    return HttpResponse(json.dumps(send_dict))

def tune(request):
    tune0 = request.POST.get('tune0', None)
    tune1 = request.POST.get('tune1', None)
    tune2 = request.POST.get('tune2', None)
    tune3 = request.POST.get('tune3', None)
    tune4 = request.POST.get('tune4', None)
    tune5 = request.POST.get('tune5', None)
    DGDPTR = 0.260924 * float(tune1) + 0.084593 * float(tune0) + 0.106020 * float(tune3) - 0.031981 * float(tune2) + 2.952166
    send_dict = {
        'success': "调整成功！",
        'output1': DGDPTR,
        'output2': tune1
    }
    return HttpResponse(json.dumps(send_dict))