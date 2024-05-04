from fastapi import FastAPI
from influxdb import InfluxDBClient
import db.dbconnect as dbc

DB_HOST = "84.247.188.251"
DB_PORT = "8086"
DB_USR = "usr"
DB_PWD = "43238c95fd3e9450"

db = dbc.DBConnector.connect(DB_HOST, DB_PORT, DB_USR, DB_PWD)
app = FastAPI()

@app.get("/dumptable/{tablename}")
async def dump_table(tablename):
    return db.dumpTable(tablename)

@app.get("/topk/{tablename}")
async def topk(tablename, k : int = 1):
    return db.topK(tablename, k)