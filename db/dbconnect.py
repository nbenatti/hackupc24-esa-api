import json
from influxdb import InfluxDBClient

class DBConnector:
    def connect(dbHost, dbPort, dbUsr, dbPwd):
        """
        Establishes a connection starting from given endpoint parameters
        """
        client = InfluxDBClient(dbHost, dbPort, dbUsr, dbPwd)
        client.switch_database("gnss_testdata")
        return DB(client)

class DB:
    def __init__(self, client):
        self.client = client

    def dumpTable(self, tableName):
        res = ""
        self.result = self.client.query("select * from " + tableName + ";")
        for table in self.result:
            for row in table:
                res += json.dumps(row)
        return res
    
    def topK(self, tableName, k):
        res = []
        self.result = self.client.query("select * from " + tableName + ";")
        for table in self.result:
            for i in range(0, k):
                res.append(table[i])
        return res
