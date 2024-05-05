import json
import scipy as sy
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
        self.windowIdx = 0

    def _computeGNSSTime(time, fullBias, bias):
        """
        Compute the GNSS time staring from raw parameters
        fetched from the GNSS chipset
        """
        return time - (fullBias + bias)
    
    def _computePseudoRange(self, txTime, rxTime):
        """
        Compute the pseudorange (i.e difference between
        satellite tx timestamp and device rx timestamp)
        """
        return ((rxTime - txTime) * sy.constants.c) / 1E9

    def _addGNSSParameters(self, result):
        """
        adds the GNSS time computations to the
        query result (must be array of dictionaries)
        """
        for record in result:
            timeNanos = record["TimeNanos"]
            timeOffsetNanos = record["TimeOffsetNanos"]
            fullBiasNanos = record["FullBiasNanos"]
            biasNanos = record["BiasNanos"]
            weekNumberNanos = 604800E9
            rx = (timeNanos + timeOffsetNanos - (fullBiasNanos + biasNanos)) - weekNumberNanos
            record["Pseudorange"] = self._computePseudoRange(record["ReceivedSvTimeNanos"], rx)
            record["GNSSTime"] = rx - timeOffsetNanos

    def _fetchAll(self):
        res = []
        for table in self.result:
            for row in table:
                res.append(row)
        self._addGNSSParameters(res)
        return res

    def dumpTable(self, tableName):
        self.result = self.client.query(f"select * from {tableName}")
        return self._fetchAll()
    
    def topK(self, tableName, k, incremental = False):
        res = []
        if incremental == False:
            self.result = self.client.query(f"select * from {tableName} order by time desc limit {k}")
            return self._fetchAll()
        else:
            if self.windowIdx < 1:
                res = []
                self.result = self.client.query(f"select * from {tableName} order by time asc")
            for table in self.result:
                for i in range(self.windowIdx*k, (self.windowIdx+1)*k):
                    res.append(table[i])
                self.windowIdx += 1
            self._addGNSSParameters(res)
            return res

    def getByConstellationType(self, tableName, constellType):
        self.result = self.client.query(f"select * from {tableName} where ConstellationType = {constellType}")
        return self._fetchAll()
    
    def getLocationsNotFurtherThan(self, threshold):
        self.result = self.client.query(f"select * from Fix where AccuracyMeters <= {threshold}")
        return self._fetchAll()