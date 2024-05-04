from influxdb import InfluxDBClient
import requests

HOST = 'localhost'
USER = 'root'
PASSWORD = 'root'
DBNAME = 'tutorial'
PORT = 8085  # setup influxdb 

client = InfluxDBClient(HOST, PORT, USER, PASSWORD, DBNAME)
client.drop_database(DBNAME)
client.create_database(DBNAME)
client.switch_database(DBNAME)

# query data
result = requests.get("http://localhost:8000/Raw/mostrecent")
json_data = result.json()
res = []
for data in json_data:
    send_data = {
        "measurement": "Raw",
        "time": data["time"],
        "fields": {
            "Cn0DbHz": data['Cn0DbHz'],
            "Pseudorange": data['Pseudorange'],
            "GNSSTIME": data['GNSSTime']
        }
    }
    res.append(send_data)
client.write_points(res)
