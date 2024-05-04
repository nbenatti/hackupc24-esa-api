from influxdb import InfluxDBClient

class DBConnector:
    def connect(dbHost, dbPort, dbUsr, dbPwd):
        """
        Establishes a connection starting from given endpoint parameters
        """
        client = InfluxDBClient(dbHost, dbPort, dbUsr, dbPwd)
        client.switch_database("gnss_testdata")
        return client

""" for table in result:
    for row in table:
        print(row) """

class DB:
    def __init__(self, client):
        self.client = client

    def dumpTable(self, tableName):
        """
        Dump all the data present 
        """
        self.result = self.client.query("select * from " + tableName + ";")
        return self.result
