import json
import boto3
import random

# configure the database
db = boto3.resource('dynamodb')
table = db.Table('ms3')


def parse_key(info, key_name):
    try:
        return info[key_name]
    except KeyError as e:
        return ""


def factory_json_communication(obj):
    json_info = []
    try:
        for d in obj:
            my_json = {
                "type": parse_key(d, "type"),
                "value": parse_key(d, "value"),
                "preferred": parse_key(d, "preferred")
            }
            json_info.append(my_json)

    except IndexError as error:
        return None

    if not json_info:
        return None
    else:
        return json_info


def factory_json_address(obj):
    json_info = []
    try:
        for d in obj:
            my_json = {
                "box": parse_key(d, "box"),
                "street": parse_key(d, "street"),
                "city": parse_key(d, "city"),
                "state": parse_key(d, "state"),
                "zip": parse_key(d, "zip"),
                "country": parse_key(d, "country"),
                "type": parse_key(d, "type")
            }
            json_info.append(my_json)

    except IndexError as error:
        return None

    if not json_info:
        return None
    else:
        return json_info


def factory_json_identification(d):
    json_info = {
        "dob": parse_key(d, "dob"),
        "firstName": parse_key(d, "firstName"),
        "lastName": parse_key(d, "lastName"),
        "jobTitle": parse_key(d, "jobTitle")
    }
    return json_info


# returns the contactId for this request.
def factory_json_contact_id(event):
    contact_id = event["contactId"]
    if contact_id == "":
        return 0
    else:
        return int(str(contact_id))


# Adds a new contact to the database.
def create_contact(event, person_json):
    # Generate new contactId for this new contact.
    person_json["contactId"] = int(str(random.random())[-12:])

    # Add new record to the database.
    table.put_item(
        Item=person_json
    )

    return {
        'statusCode': 201,
        'body': 'new contact created - ' + str(person_json["contactId"]),
        'name': json.dumps(person_json)
    }


# Edits an existing contact.
def edit_contact(event, person_json):
    contact_id = factory_json_contact_id(event)
    if contact_id == 0:
        return {
            'statusCode': 404,
            'body': 'not found'
        }

    response = table.update_item(
        Key={
            'contactId': contact_id
        },
        UpdateExpression="set "
                         "identification=:i, "
                         "communication=:c, "
                         "address=:a",
        ExpressionAttributeValues={
            ':i': person_json["identification"],
            ':c': person_json["communication"],
            ':a': person_json["address"]
        },
        ReturnValues="UPDATED_NEW"
    )

    return {
        'statusCode': 200,
        'body': 'contact edited - ' + str(contact_id)
    }


def delete_contact(event):
    contact_id = factory_json_contact_id(event)
    if contact_id == 0:
        return {
            'statusCode': 404,
            'body': 'not found'
        }

    try:
        response = table.delete_item(
            Key={
                'contactId': contact_id
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        return {
            'statusCode': 200,
            'body': 'contact deleted'
        }


# def get_json_tree_branch(event, branch_name):
#     try:
#         x = event[branch_name]
#         if x == '':
#             return [{}]
#
#     except IndexError as error:
#         return [{}]
#     else:
#         return [{}]


# Main for AWS Lambda.
def lambda_handler(event, context):
    # blank contact template
    person_json = {"contactId": 0, "identification": {}, "address": [], "communication": []}

    # Validate the data, and construct a new JSON contact object.
    c_json = factory_json_communication(event['communication'])
    if c_json is not None:
        person_json["communication"].extend(c_json)

    p_json = factory_json_address(event['address'])
    if p_json is not None:
        person_json["address"].extend(p_json)

    person_json["identification"] = factory_json_identification(event['identification'])
    person_json["contactId"] = factory_json_contact_id(event)

    # Determine the action needed.  create, edit, delete.
    post_action = event['awsAction']

    if post_action == "create":
        return create_contact(event, person_json)

    elif post_action == "edit":
        return edit_contact(event, person_json)

    elif post_action == "delete":
        return delete_contact(event)

    else:
        return {
            'statusCode': 200,
            'body': 'no action'
        }
