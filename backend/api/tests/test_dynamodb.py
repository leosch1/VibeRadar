import boto3

session = boto3.Session(
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='eu-west-1'
)

dynamodb = session.resource('dynamodb', endpoint_url='http://localhost:4566')
table = dynamodb.Table('Cities')

try:
    response = table.scan()
    items = response.get('Items', [])
    print(f"Found {len(items)} item(s).")
    for item in items:
        print(item)
except Exception as e:
    print(f"Error scanning table: {e}")
