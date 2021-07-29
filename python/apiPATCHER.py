from submodules.pyvidesk.pyvidesk import Pyvidesk
import boto3
import requests
import json

def get_token(name):
    client = boto3.client("ssm", region_name='sa-east-1')
    response = client.get_parameter(Name= name, WithDecryption=True)
    KEY = response['Parameter']['Value']
    return KEY

def api_data(MVTOKEN):
    persons = Pyvidesk(token= MVTOKEN).persons 
    persons_properties = persons.get_properties()
    query = (
    persons.query.filter(
        persons_properties['personType'] == 2
    )
    .select(persons_properties['cpfCnpj'])
    .select(persons_properties['businessName'])
    .select(persons_properties['customFieldValues'])
    .expand(persons_properties['customFieldValues'])
    )
    print(query.as_url())
    data = query.all()
    return data

def file_reader(file):
    with open(file, 'r', encoding='utf-8') as fd:
        raw_data = fd.readlines()
    data = [it.strip().split(",") for it in raw_data[1:]]

    return data

TOKEN = get_token('MovideskAPIKey')
data_1 = api_data(TOKEN)
data_2 = file_reader('data.csv')
counter = 0 

#print(data)

body = {
    "businessName": "",
    "cpfCnpj": "",
    "id": "",
    "customFieldValues": [
        {
            "customFieldId": 82744,
            "customFieldRuleId": 40423,
            "line": 1,
            "value": ""
        }
    ]
}

# for model in data_1:
#     for field in model.customFieldValues:
#         print(field.value)

 

for data in data_2:
    for model in data_1:
        if model.businessName == data[0] or model.cpfCnpj == data[3]:
            body['businessName'] = model.businessName
            body['cpfCnpj'] = model.cpfCnpj
            body['id'] = model.id
            for field in body['customFieldValues']:
                field['value'] = data[1]
            counter += 1
            req_body = json.dumps(body)
            request_link = f'https://api.movidesk.com/public/v1/persons?token={TOKEN}&id={model.id}'
            r = requests.patch(request_link, data = json.dumps(body), headers={'Content-Type':'application/json'})
            #print(request_link)
            #print(r.url)
            print(r.content)
            #print(req_body)
print(counter)

