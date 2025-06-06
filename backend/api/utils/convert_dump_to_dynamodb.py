import boto3
import csv
import re

session = boto3.Session(
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='eu-west-1'
)
dynamodb = session.resource('dynamodb', endpoint_url='https://localhost.localstack.cloud:4566')

# Define the table schema
table_name = 'Cities'
existing_tables = list(dynamodb.tables.all())
if table_name not in [t.name for t in existing_tables]:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'},
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.wait_until_exists()
    print(f"Table '{table_name}' created.")
else:
    table = dynamodb.Table(table_name)
    print(f"Table '{table_name}' already exists.")

def parse_copy_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tables = {}
    matches = re.findall(r"COPY public\.(\w+) \((.*?)\) FROM stdin;\n(.*?)\\\.", content, re.DOTALL)
    for table_name, columns_str, data_str in matches:
        columns = [col.strip() for col in columns_str.split(',')]
        rows = list(csv.reader(data_str.strip().split('\n'), delimiter='\t'))
        tables[table_name] = [dict(zip(columns, row)) for row in rows]
    return tables

def upload_to_dynamodb(table, items):
    for item in items:
        # Remove nulls and binary PostGIS data
        item = {k: v for k, v in item.items() if v and not v.startswith('0101')}
        try:
            table.put_item(Item=item)
        except Exception as e:
            print(f"Failed to insert item: {item}\nError: {e}")

data = parse_copy_lines('api/sql/02_backup.sql')

if 'cities' in data:
    upload_to_dynamodb(table, data['cities'])

print(f"Uploaded {len(data['cities'])} items to DynamoDB table '{table_name}'.")