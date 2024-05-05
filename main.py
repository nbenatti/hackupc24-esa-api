from fastapi import FastAPI
from influxdb import InfluxDBClient
import db.dbconnect as dbc

DB_HOST = "84.247.188.251"
DB_PORT = "8086"
DB_USR = "usr"
DB_PWD = "43238c95fd3e9450"

db = dbc.DBConnector.connect(DB_HOST, DB_PORT, DB_USR, DB_PWD)
app = FastAPI()

@app.get("/{tablename}/dumptable")
async def dump_table(tablename):
    return db.dumpTable(tablename)

@app.get("/{tablename}/mostrecent")
async def topk(tablename, k : int = 1):
    return db.topK(tablename, k, False)

@app.get("/{tablename}/mostrecent/incr")
async def topk(tablename, k : int = 1):
    return db.topK(tablename, k, True)

@app.get("/{tableName}/constellation/")
async def get_by_constellation_type(tableName, type : int = 1):
    return db.getByConstellationType(tableName, type)

@app.get("/getlocations")
async def get_locations(threshold : float = 1.0):
    return db.getLocationsNotFurtherThan(threshold)
