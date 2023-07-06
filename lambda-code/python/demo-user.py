import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("demo-user")

# ユーザーTBL操作Lambda
def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    OperationType = event['OperationType']
    try:
        if OperationType == 'SCAN':
            return operation_scan()
            
        PartitionKey = event['Keys']['userId']

        if OperationType == 'QUERY':
            return operation_query(PartitionKey)
        
        elif OperationType == 'PUT':
            UserName = event['Keys']['userName']
            MailAdress = event['Keys']['mailAdress']
            return operation_put(PartitionKey, UserName, MailAdress)
        
        elif OperationType == 'DELETE':
            return operation_delete(PartitionKey)

    except Exception as e:
        print("Error Exception.")
        print(e)


# テーブルスキャン
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return items

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        KeyConditionExpression = Key("userId").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

# レコード追加・更新
def operation_put(partitionKey, userName, mailAdress):
    putResponse = table.put_item(
        Item={
            'userId': partitionKey,
            'userName': userName,
            'mailAdress': mailAdress
        }
    )
    if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(putResponse)
    else:
        print('PUT Successed.')
    return putResponse

# レコード削除
def operation_delete(partitionKey):
    delResponse = table.delete_item(
       key={
           'userId': partitionKey,
       }
    )
    if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        print(delResponse)
    else:
        print('DEL Successed.')
    return delResponse

