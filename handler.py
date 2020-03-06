from lxml import html
import requests
import boto3

sns_topic = 'SNS:ARN:GOES:HERE'
sns = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('prime_ministers')

def test_pm(tree, pm_xpath, pm_value_xpath):
    wiki_pm_name_array = tree.xpath(pm_xpath)
    wiki_pm_name = wiki_pm_name_array[0]
    wiki_pm_party_array = tree.xpath(pm_value_xpath)
    wiki_pm_party = wiki_pm_party_array[0]

    response = table.get_item(Key={'name': wiki_pm_name})
    ddb_pm_party = response['Item']['party']

    print('Wikipedia PM name: ' + wiki_pm_name)
    print('Wikipedia PM party: ' + wiki_pm_party)
    print('DDB PM party: ' + ddb_pm_party)

    # test if different to previous value
    if (wiki_pm_party != ddb_pm_party):
        print('ALERT!')
        response = sns.publish(
            TopicArn=sns_topic,
            Message='Prime Minister party change!',
            Subject='Email'
        )
        print(response)

        # Set new ddb value
        response = table.put_item(Item=
            {
                'name': wiki_pm_name,
                'party': wiki_pm_party
            }
        )
        print(response)

def handler(event, context):
    page = requests.get('https://en.wikipedia.org/wiki/Prime_Minister_of_Australia')
    tree = html.fromstring(page.content)

    # Edmund Barton
    test_pm(tree, '/html/body/div[3]/div[3]/div[4]/div/table[5]/tbody/tr[2]/td[1]/a/text()',
            '/html/body/div[3]/div[3]/div[4]/div/table[5]/tbody/tr[2]/td[3]/a/text()')

    # Alfred Deakin
    test_pm(tree, '/html/body/div[3]/div[3]/div[4]/div/table[5]/tbody/tr[3]/td[1]/a/text()',
            '/html/body/div[3]/div[3]/div[4]/div/table[5]/tbody/tr[3]/td[3]/a/text()')

    response = {
        "statusCode": 200,
        "body": "Function executed successfully"
    }

    return response

if __name__== "__main__":
    print(handler('',''))