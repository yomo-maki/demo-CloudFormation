import json
import boto3

from boto3.dynamodb.conditions import Key
# Keyオブジェクトを利用できるようにする

# Dynamodbアクセスのためのオブジェクト取得
dynamodb = boto3.resource('dynamodb')
# 指定テーブルのアクセスオブジェクト取得
table = dynamodb.Table("demo-product")


# 商品TBL-GSI検索用
def lambda_handler(event, context):
  print("Received event: " + json.dumps(event))
  OperationType = event['OperationType']
  try:
      if OperationType == 'SCAN':
          return operation_scan()

      PartitionKey = event['Keys']['productCategory']
      if OperationType == 'QUERY':
          return operation_query(PartitionKey)
      
  except Exception as e:
      print("Error Exception.")
      print(e)

# テーブルスキャン
def operation_scan():
    scanData = table.scan()
    items=scanData['Items']
    print(items)
    return scanData

# レコード検索
def operation_query(partitionKey):
    queryData = table.query(
        IndexName = 'productCategory-index',
        KeyConditionExpression = Key("productCategory").eq(partitionKey)
    )
    items=queryData['Items']
    print(items)
    return items

