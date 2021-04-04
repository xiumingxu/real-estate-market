import csv
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine
import yaml
import os, sys


# default is mysql
class DBUpdater:
    def __init__(self, database="HOUSING"):
        self.cred_file = "creds.yaml"
        # validate cred file
        if not os.path.exists(self.cred_file):
            FileNotFoundError("creds.yaml not found: did you rename creds_template.yaml?")
        user, password, host = self.parse_creds(database)
        self._mysql_connect(host, user, password, database)

    def _mysql_connect(self, host, user, password, database):
        # if using mysql-connector-python (causes problems with pd.read_sql_query for gui).
        # conn = mysql.connector.connect(host=server, user=user, password=password, database=database, use_pure=True)
        # conn = pymysql.connect(host=host, user=user, password=password, db=database)
        self.conn = create_engine(
            f"mysql://{user}:{password}@{host}/{database}")  # enter your password and database names here

    def properSep(self, data):
        return data.str.split('[,](?:\d)').apply(pd.Series)

    def save_csv(self, filename):
        df = pd.read_csv(filename, sep=',', quotechar='"', skipinitialspace=True,  dtype='unicode', encoding='utf-8')  # Replace Excel_file_name with your excel sheet name
        self.save_df(filename, df)  # Replace Table_name with your sql table name
        # cursor = conn.cursor()
        # return conn, cursor
    def save_df(self, filename, df):
        tablename = filename[:-4]
        df.to_sql(tablename, con=self.conn, index=False, if_exists='replace')


    def parse_creds(self, database_name):
        base_path = Path(__file__).parent
        path = Path.resolve(base_path / self.cred_file)
        with open(path, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        # database creds
        user = data['databases'][database_name]['user']
        password = data['databases'][database_name]['password']
        host = data['databases'][database_name]['host']

        # # datasource creds
        # data_source_info = {}
        # for datasource in data['datasources']:
        #     data_source_info[datasource] = data['datasources'][datasource]

        return user, password, host

