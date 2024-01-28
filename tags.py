
import json
import pandas as pd
from collections import defaultdict
from copy import deepcopy

def get_json(path):
    file = open(path, encoding="UTF-8")
    data = json.load(file)
    file.close()    
    return data
    
def tags_to_csv(data):
    insert_topics, move_topics = [],[]

    for operation in data["operations"]:
        if operation["operation"] == "insert_topic":
            insert_topics.append(operation["topic"])
        if operation["operation"] == "move_topics":
            move_topics.append({"parentLabel": operation["parentLabel"], "childLabels": operation["childLabels"]})

    df_insert_topics = pd.DataFrame(insert_topics)
    df_move_topics = pd.DataFrame(move_topics).explode("childLabels")
    
    df_move_topics.to_csv('parent_topics_topic.csv',sep=',')



def tags_to_json(path):
    file = open(path, encoding="UTF-8")
    data = json.load(file)    
    lista = []

    for node in data['rootNodes']:
        ddict = defaultdict(str)
        ddict["name"] = node
        for operation in data["operations"]:
            if operation["operation"] == "move_topics":
                if operation["parentLabel"] == node:
                    children = [{"name": child, "children":[]} for child in operation["childLabels"]]
                    ddict["children"] = children
                    for inner_child in children:
                        for operation in data["operations"]:
                            if operation["operation"] == "move_topics":
                                if inner_child['name'] == operation["parentLabel"]:
                                    inner_child['children'] = [{"name": nieto, "children":[]} for nieto in operation["childLabels"]]
        lista.append(ddict)                
    with open('tags_v1.json', 'w', encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)
    
def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for item in data:
                [rows.append(elem) for elem in flatten_list(flatten_json(item, prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pd.DataFrame(flatten_json(data_in))




if __name__ == '__main__':
    tags_to_json("./Json/General Oct 2023 v2.json")
    json_data = get_json('tags_v1.json')
    df = json_to_dataframe(json_data)
    df.to_csv('new_parent_topics_topic.csv',sep=',')