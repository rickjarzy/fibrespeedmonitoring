import os
import logging
import traceback
import time
import psutil
import pytz
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from speedtest import Speedtest, SpeedtestException, ConfigRetrievalError


def make_speed_test() -> dict:
    speedtest = Speedtest()
    time_now = datetime.now()
    print("Start testing internet connection ...")
    dl_speed = speedtest.download() / 1000000  # Convert to Mbps
    ul_speed = speedtest.upload() / 1000000  # Convert to Mbps
    best_servers = speedtest.get_best_server()

    pass

def main() -> None:
    token:str = os.getenv("INFLUXDB_HIGHHILL_API_TOKEN")
    org:str = os.getenv("INFLUXDB_HIGHHILL_ORG")
    bucket:str = os.getenv("INFLUXDB_HIGHHILL_BUCKET")
    logging.info(f"org: {org}")
    with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:
        with client.write_api(write_options=SYNCHRONOUS) as write_api:
            while True:
                
                cpu_temperatures = psutil.sensors_temperatures()
                for core in cpu_temperatures["coretemp"]:
                    logging.info(f"""{core.label} - {core.current} - {datetime.now().isoformat()}""")
                    
                    p = Point("cpu_temp")\
                        .tag("location", f"{core.label}")\
                        .field("core_temp", core.current)\
                        .time(int(datetime.now(tz=pytz.timezone('Europe/Vienna')).timestamp()), WritePrecision.S)
                        #.time(datetime.now().isoformat())
                        
                    write_api.write(bucket=bucket, 
                                    org=org, 
                                    record=p
                                    )
                time.sleep(15)

    logging.info("PROGRAMM ENDE")

if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO)
        main()
    except KeyboardInterrupt:
        logging.error("\n# Programm terminated by User")
    except Exception as e:
        logging.error(f"### ERROR - something went wrong : {e}")
        traceback.print_exc()


