import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)
table_name = "todo_list"


class DynamoDB():
    def __init__(self):
        session = boto3.Session(
            aws_access_key_id="AKIAX7MFXFJLFOAQRYN5",
            aws_secret_access_key="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",
            region_name="us-east-1"
        )

        client = session.resource('dynamodb')
        self.table = client.Table(table_name)

    def exists(self):
        print(self.table.creation_date_time)

    def getListItem(self):
        response = self.table.scan()
        items = response['Items']
        return items
        

    def addItem(self, content):
        try:
            id = self.getListItem()
            dateTimeObj = datetime.now()
            self.table.put_item(
                Item={
                    'id': str(len(id)),
                    'content': content,
                    'date_created': dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)"),
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't add data to table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def getItem(self, id):
        try:
            response = self.table.get_item(
                Key={
                    'id': str(id),
                }
            )

        except ClientError as err:
            logger.error(
                "Couldn't fetch data from table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            item = response['Item']
            print(item)
            return item

    def delteItem(self, id):
        try:
            self.table.delete_item(
                Key={
                    'id': str(id),
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't delete data from table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def updateItem(self, id, content):
        try:
            self.table.update_item(
                Key={
                    'id': str(id),
                },
                UpdateExpression='SET content = :val1',
                ExpressionAttributeValues={
                    ':val1': content
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't update data for table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
