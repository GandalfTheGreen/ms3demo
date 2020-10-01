import json
import boto3

db = boto3.resource('dynamodb')
table = db.Table('ms3')


def all_contacts():
    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return {
            'statusCode': 200,
            'people': response['Items']
        }


def single_contact(my_year):
    try:
        response = table.get_item(Key={'contactId': my_year})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return {
            'statusCode': 200,
            'people': response['Item']
        }


def lambda_handler(event, context):
    # query_contact_id = event["queryStringParameters"]["contactid"]
    query_contact_id = None

    # is this request for a specific contact id?
    if query_contact_id != None:
        try:
            my_year = int(query_contact_id)
            return single_contact(my_year)
        except ClientError as e:
            print('error')
    else:
        return all_contacts()
