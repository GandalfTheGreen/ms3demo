# ms3demo
This demo was created for MS3.

## Example React application
An example React application was created for this API.  (Contact Brian if you need the URL.). It uses an S3 Bucket to host the "serverless" application.  It  uses the API Gateway and Lambda functions.  Contacts are stored in DynamoDB.

## AWS Lambda - ms3toc.py
Reads the table from DynamoDB, and returns a list of contacts in JSON format.

## AWS Lambda - ms3store.py
Create, Update, Delete contacts in the database.  Example JSON object:


```json
{
    "awsAction": "update",
    "contactId": "1234",
  "address": [
    {
      "box": "2509",
      "city": "Charleston",
      "country": "USA",
      "state": "WV",
      "street": "Mountaineer Blvd",
      "type": "business",
      "zip": "25309"
    },
    {
      "box": "100",
      "city": "Charleston",
      "country": "USA",
      "state": "WV",
      "street": "Main Street",
      "type": "business",
      "zip": "25309"
    }
  ],
  "communication": [
    {
      "preferred": "true",
      "type": "email",
      "value": "alexa@sample.com"
    },
    {
      "type": "phone",
      "value": "222-555-2222"
    }
  ],
  "identification": {
    "dob": "2002-02-02",
    "firstName": "Alexa",
    "jobTitle": "Sales",
    "lastName": "Powell"
  }
}
```

Brian Green
