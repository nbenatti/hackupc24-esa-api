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

    def _fetchAll(self):
        res = []
        for table in self.result:
            for row in table:
                res.append(row)
        return res

    def dumpTable(self, tableName):
        self.result = self.client.query(f"select * from {tableName}")
        return self._fetchAll()
    
    def topK(self, tableName, k):
        res = []
        self.result = self.client.query(f"select * from {tableName}")
        for table in self.result:
            for i in range(0, k):
                res.append(table[i])
        return res

    def getByConstellationType(self, tableName, constellType):
        self.result = self.client.query(f"select * from {tableName} where ConstellationType = {constellType}")
        return self._fetchAll()