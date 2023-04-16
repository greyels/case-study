import datetime
import json
import os
import statistics
from typing import Union

import sqlalchemy
from google.cloud import storage


def transform_json(event: dict, context) -> str:
    client = storage.Client()
    bucket = client.bucket(event['bucket'])
    blob = bucket.blob(event['name'])

    contents_dict = json.loads(blob.download_as_string())
    try:
        timestamp = contents_dict['time_stamp']
        data = contents_dict['data']
    except KeyError:
        raise Exception('Timestamp or data is not found in the JSON file!')

    timestamp_utc = calc_ts_utc(timestamp)
    mean = std_dev = None
    if data:
        mean = statistics.mean(data)
        std_dev = statistics.stdev(data)
    return insert_to_mysql(timestamp_utc, mean, std_dev)


def calc_ts_utc(timestamp: str) -> str:
    timestamp_local = datetime.datetime.fromisoformat(timestamp)
    return str(timestamp_local.astimezone(datetime.timezone.utc))


def insert_to_mysql(timestamp: str, mean: Union[str, None], std_dev: Union[str, None]) -> str:
    table_name = os.environ.get('TABLE_NAME')
    query = f"INSERT INTO {table_name} (timestamp, mean, std_dev) VALUES ('{timestamp}', {mean}, {std_dev})"
    stmt = sqlalchemy.text(query)

    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS"),
            database=os.environ.get("DB_NAME"),
            query=dict({"unix_socket": f"/cloudsql/{os.environ.get('CONN_NAME')}"}),
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800
    )
    try:
        with db.connect() as conn:
            conn.execute(stmt)
    except Exception as e:
        return f"Error: {str(e)}"
    return "JSON file transformed and inserted successfully!"
