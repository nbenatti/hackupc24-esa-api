import fastapi
from influxdb import InfluxDBClient
import db.dbconnect as dbc

DB_HOST = "84.247.188.251"
DB_PORT = "8086"
DB_USR = "usr"
DB_PWD = "43238c95fd3e9450"

db = dbc.DBConnector.connect(DB_HOST, DB_PORT, DB_USR, DB_PWD)