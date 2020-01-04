import boto3
import feedparser
import json
from dateutil import parser

def lambda_handler(event, context):
    """
    :type event: object
    :param event:
    :param context:
    :return:
    """
    boto3.setup_default_session(profile_name='awsbot')
    dynamodb = boto3.client('dynamodb')
    for object in event:
        feed = feedparser.parse(object['rss_url'])
        for item in feed["items"]:
            try:
                id = item['id']
                author = item['author']
                published = parser.parse(item['published']).isoformat()
                link = item['link']
                title = item['title']
                channel_version = feed["version"]
                channel_title = feed["channel"]["title"]
                channel_description = feed["channel"]["description"]
                channel_link = feed["channel"]["link"]

                if item['summary'] != "":
                    summary = item['summary']
                else:
                    summary = item['title']

                if item['tags']:
                    term = item['tags'][0]['term']\
                        .replace("general:products/", "")\
                        .replace("-", " ")\
                        .title()\
                        .replace("Aws", "AWS")\
                        .replace("Ec2", "EC2")\
                        .replace("Rds", "RDS")\
                        .replace("Vpc", "VPC") \
                        .replace("Iot", "IoT") \
                        .split(",")[0]
                else:
                    term = 'New'

                response = dynamodb.put_item(
                    TableName=object['table_name'],
                    ConditionExpression='attribute_not_exists(id)',
                    Item={
                        'id': {
                            'S': id
                        },
                        'author': {
                            'S': author
                        },
                        'published': {
                            'S': published
                        },
                        'link': {
                            'S': link
                        },
                        'summary': {
                            'S': summary
                        },
                        'title': {
                            'S': title
                        },
                        'term': {
                            'S': term
                        },
                        'channel_version': {
                            'S': channel_version
                        },
                        'channel_title': {
                            'S': channel_title
                        },
                        'channel_description': {
                            'S': channel_description
                        },
                        'channel_link': {
                            'S': channel_link
                        }
                    }
                )
            except dynamodb.exceptions.ConditionalCheckFailedException as e:
                pass
            except Exception as e:
                print e

if __name__ == "__main__":
    with open('event.json') as json_file:
        event = json.loads(json_file.read())
    lambda_handler(event, '')
