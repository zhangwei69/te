import os
import json
import requests

# notion基本参数
token = os.getenv("NotionToken")
headers = {
    'Notion-Version': '2022-02-22',
    'Authorization': 'Bearer ' + token,
}
def DataBase_item_query(query_database_id):
    url_notion_block = 'https://api.notion.com/v1/databases/'+ query_database_id +'/query'
    res_notion = requests.post(url_notion_block, headers=headers)
    S_0 = res_notion.json()
    res_travel = S_0['results']
    if_continue = len(res_travel)
    if if_continue > 0:
        while if_continue % 100 == 0:
            body = {
                'start_cursor' : res_travel[-1]['id']
            }
            res_notion_plus = requests.post(url_notion_block,headers=headers,json = body)
            S_0plus = res_notion_plus.json()
            res_travel_plus = S_0plus['results']
            for i in res_travel_plus:
                if i['id'] == res_travel[-1]['id']:
                    continue
                res_travel.append(i)
            if_continue = len(res_travel_plus)
    return res_travel

def DataBase_additem(database_id, body_properties, station):
    body = {
        'parent': {'type': 'database_id', 'database_id': database_id},
    }
    body.update(body_properties)
    
    url_notion_additem = 'https://api.notion.com/v1/pages'
    notion_additem = requests.post(url_notion_additem,headers=headers,json=body)

    if notion_additem.status_code == 200:
        return station+'·更新成功 开始每日自动打卡！'
    else:
        return station+'·更新失败'

def body_properties_input(body,label,type_x,data):
    headers['Notion-Version']  = '2021-05-13'

    if type_x == 'checkbox':
        body['properties'].update({label:{'type': 'checkbox', 'checkbox': data}})

    if type_x == 'date':
        body['properties'].update({label:{'type': 'date', 'date': {'start': data, 'end': None}}})

    if type_x == 'select':
        body['properties'].update({label:{'type': 'select', 'select': {'name': data}}})

    if type_x == 'rich_text':
        body['properties'].update({label:{'type': 'rich_text', 'rich_text': [{'type': 'text', 'text': {'content': data},  'plain_text': data}]}})

    if type_x == 'title':
        body['properties'].update({label:{'id': 'title', 'type': 'title', 'title': [{'type': 'text', 'text': {'content': data}, 'plain_text': data}]}})

    if type_x == 'number':
        body['properties'].update({label:{'type': 'number', 'number': data}})

    return body

def datafresh(jsondata):
    result = []
    for item in jsondata:
        dict = {}
        try:
            dict["StuID"] = item["properties"]["StuID"]["title"][0]["plain_text"]
        except:
            continue
        dict["password"] = item["properties"]["password"]["rich_text"][0]["plain_text"]
        dict["cookie"] = item["properties"]["cookie"]["rich_text"][0]["plain_text"]
        dict["checkdaily"] = item["properties"]["checkdaily"]["rich_text"][0]["plain_text"]
        dict["chat_id"] = item["properties"]["chat_id"]["rich_text"][0]["plain_text"]
        result.append(dict)
    return result