import json
import boto3
import os
import requests


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    global fromFbId
    fromFbId = "209806693253652"
    global userTable
    userTable = dynamodb.Table(os.environ['message_table'])
    if event['httpMethod'] == 'POST':
        if event['body']:
            print(event['body'])
            body = json.loads(event['body'])

            if body.get('message_uuid'):
                print('Received an outbound message event!')

            if body.get('msisdn'):
                print('Received an inbound text message!')
                item = findUser(number=str(body['msisdn']))
                user = item['user']
                message = body['text']
                item['message'] = message
                print(f"New item: {item}")
                userTable.put_item(
                    Item=item
                )

                # Get everyone in the table that is not the person that sent this message
                response = userTable.scan(
                    FilterExpression="NOT contains(#user_alias, :u)",
                    ExpressionAttributeValues={
                        ":u": user
                    },
                    ExpressionAttributeNames= {
                        "#user_alias": "user"
                    }
                )
                for item in response['Items']:
                    userNumber = item.get('number')
                    userFbId = item.get('fbid')
                    print(f"Sending a message to: {item['user']}")
                    if item['user'] == "john":
                        fromNumber = "12013451218"
                    else:
                        fromNumber = "447418342701"
                    payload = {
        "template":"failover",
        "workflow": [
        {
            "from": { "type": "messenger", "id": f"{fromFbId}" },
            "to": { "type": "messenger", "id":  f"{userFbId}"},
            "message": {
            "content": {
                "type": "text",
                "text": f"{message}"
            }
            },
            "failover":{
            "expiry_time": 600,
            "condition_status": "delivered"
            }
        },
        {
            "from": {"type": "sms", "number": f"{fromNumber}"},
            "to": { "type": "sms", "number": f"{userNumber}"},
            "message": {
            "content": {
                "type": "text",
                "text": f"{message}"
            }
            }
        }
        ]
    }
                    headers = {'Authorization': f"Bearer {os.environ['JWT']}", 'Content-Type': 'application/json', 'Accept': 'application/json'}
                    
                    response = requests.post('https://api.nexmo.com/v0.1/dispatch',
                                json=payload, headers=headers)

                    print (response.text)
                    return {
                        'statusCode': 200
                    }

            if body.get('to'):
                if body['to'].get('type') == "messenger":
                    userFbId = body['from']['id']
                    print (f"Received an inbound Facebook Messenger message from {userFbId}")
                    message = body['message']['content']['text']
                    item = findUser(fbid=str(userFbId))
                    user = item['user']
                    print (f"User is: {user}")

                    # Upload new item to DynamoDB with new message
                    item['message'] = message
                    print(f"New item: {item}")
                    userTable.put_item(
                        Item=item
                    )
                    # Get everyone in the table that is not the person that sent this message
                    response = userTable.scan(
                        FilterExpression="NOT contains(#user_alias, :u)",
                        ExpressionAttributeValues={
                            ":u": user
                        },
                        ExpressionAttributeNames= {
                            "#user_alias": "user"
                        }
                    )
                    for item in response['Items']:
                        userNumber = item.get('number')
                        userFbId = item.get('fbid')
                        print(f"Sending a message to: {item['user']}")
                        if item['user'] == "john":
                            fromNumber = "12013451218"
                        else:
                            fromNumber = "447418342701"
                        payload = {
            "template":"failover",
            "workflow": [
            {
                "from": { "type": "messenger", "id": f"{fromFbId}" },
                "to": { "type": "messenger", "id":  f"{userFbId}"},
                "message": {
                "content": {
                    "type": "text",
                    "text": f"{message}"
                }
                },
                "failover":{
                "expiry_time": 600,
                "condition_status": "delivered"
                }
            },
            {
                "from": {"type": "sms", "number": f"{fromNumber}"},
                "to": { "type": "sms", "number": f"{userNumber}"},
                "message": {
                "content": {
                    "type": "text",
                    "text": f"{message}"
                }
                }
            }
            ]
        }
                        headers = {'Authorization': f"Bearer {os.environ['JWT']}", 'Content-Type': 'application/json', 'Accept': 'application/json'}
                        
                        response = requests.post('https://api.nexmo.com/v0.1/dispatch',
                                    json=payload, headers=headers)

                        print (response.text)
                    
            if body.get('sendMessage'):
                user = body['sendMessage']
                if user == "john":
                    fromNumber = "12013451218"
                else:
                    fromNumber = "447418342701"
                message = body['message']
                response = userTable.get_item(
                    Key={
                        'user': user
                    }
                )
                userNumber = response['Item'].get('number')
                userFbId = response['Item'].get('fbid')
                print(f"Sending a message to: {body['sendMessage']}")
                payload = {
    "template":"failover",
    "workflow": [
      {
        "from": { "type": "messenger", "id": f"{fromFbId}" },
        "to": { "type": "messenger", "id": f"{userFbId}" },
        "message": {
          "content": {
            "type": "text",
            "text": f"{message}"
          }
        },
        "failover":{
          "expiry_time": 600,
          "condition_status": "delivered"
        }
      },
      {
        "from": {"type": "sms", "number": f"{fromNumber}"},
        "to": { "type": "sms", "number": f"{userNumber}"},
        "message": {
          "content": {
            "type": "text",
            "text": f"{message}"
          }
        }
      }
    ]
  }
                headers = {'Authorization': f"Bearer {os.environ['JWT']}", 'Content-Type': 'application/json', 'Accept': 'application/json'}
                
                response = requests.post('https://api.nexmo.com/v0.1/dispatch',
                              json=payload, headers=headers)

                print (response.text)

            if body.get('getUsers'):
                print(f"Getting all users in the table")
                response = userTable.scan()
                return {
                    'statusCode': 200,
                    'body': json.dumps({'users': response['Items']})
                }

            if body.get('pollUser'):
                print(f"Getting the message for: {body['pollUser']}")
                response = userTable.get_item(
                    Key={
                        'user': body['pollUser']
                    }
                )
                print(response)
                message = response['Item'].get('message')
                if message:
                    del response['Item']['message']
                    item = response['Item']
                    userTable.put_item(
                        Item=item
                    )
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': message})
                    }

                if not message:
                    return {
                        'statusCode': 200,
                        'body': json.dumps({'message': False})
                    }
            return {
                'statusCode': 200
            }

    elif event['httpMethod'] == 'GET':
        return {
            'statusCode': 200
        }


def findUser(number=None, fbid=None):
    response = userTable.scan()
    print(response['Items'])
    if number:
        for item in response['Items']:
            if item.get('number') == number:
                return item
    if fbid:
        for item in response['Items']:
            if item.get('fbid') == fbid:
                return item