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
while(True):
    result = requests.get("http://localhost:8000/Raw/mostrecent/incr?k=5")
    json_data = result.json()
    res = []
    for data in json_data:
        send_data = {
            "measurement": "Raw",
            "time": data["time"],
            "fields": {
                "Cn0DbHz": data['Cn0DbHz'],
                "ConstellationType": data['ConstellationType'],
                "SvidTag": data['SvidTag'],
                "Pseudorange": data['Pseudorange'],
                "GNSSTime": data['GNSSTime']
            }
        }
        print(send_data)
        res.append(send_data)
    client.write_points(res)
