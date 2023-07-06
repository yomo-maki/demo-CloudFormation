import json
import boto3

from datetime import datetime

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("demo-product")


# 商品TBL操作Lambda
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  now = datetime.now()
  print(now)
  OperationType = event['OperationType']

  try:
    if OperationType == 'SCAN':
      return operation_scan()

    elif OperationType == 'QUERY':
      PartitionKey = event['Keys']['productId']
      return operation_query(PartitionKey)

    elif OperationType == 'PUT':
      PartitionKey = event['Keys']['productContributorId'] + str(now)
      return post_product(PartitionKey, event)

    elif OperationType == 'DELETE':
      return operation_delete(PartitionKey)

  except Exception as e:
      print("Error Exception.")
      print(e)


# テーブルスキャン
def operation_scan():
  scanData = table.scan()
  items = scanData['Items']
  print(items)
  return items

# レコード検索
def operation_query(partitionKey):
  queryData = table.query(
      KeyConditionExpression = Key("productId").eq(partitionKey)
  )
  items=queryData['Items']
  print(items)
  return items

# レコード追加
def post_product(PartitionKey, event):
  putResponse = table.put_item(
    Item={
      'productId' : PartitionKey,
      'productName' : event['Keys']['productName'],
      'productCategory' : event['Keys']['productCategory'],
      'productContributor' : event['Keys']['productContributor'],
      'productContributorId' : event['Keys']['productContributorId'],
      'productExplanation' : event['Keys']['productExplanation'],
      'productImageUrl' : event['Keys']['productImageUrl'],
      'productQuantity' : event['Keys']['productQuantity']
    }
  )
  
  if putResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
    print(putResponse)
  else:
    print('Post Successed.')
  return putResponse

# レコード削除
def operation_delete(partitionKey):
  delResponse = table.delete_item(
     key={
         'productId': partitionKey,
     }
  )
  if delResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
      print(delResponse)
  else:
      print('DEL Successed.')
  return delResponse


