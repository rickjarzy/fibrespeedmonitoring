import time
import traceback
from datetime import datetime
from speedtest import Speedtest, SpeedtestException, ConfigRetrievalError


def main() -> None:
    try:
        while True:

            speedtest = Speedtest()
            time_now = datetime.now()
            print("Start testing internet connection ...")
            dl_speed = speedtest.download() / 1000000  # Convert to Mbps
            ul_speed = speedtest.upload() / 1000000  # Convert to Mbps
            best_servers = speedtest.get_best_server()
            all_servers = speedtest.get_servers()

            print("Download Speed: {:.2f}".format(dl_speed) + f" Mbps\t- {time_now}")
            print("Upload Speed: {:.2f}".format(ul_speed) + f" Mbps\t- {time_now}")
            for element in all_servers:
                print(f"Used Server: {element}")
                print(all_servers[element])
            print(f"Best Server used: {best_servers}")
            time.sleep(30)

    except Exception as e:
        print(f"### ERROR - something went wrong {e}")
        traceback.print_exc()
        print("Restarting speedtest in 30 seconds")
        time.sleep(30)
        main()
    except KeyboardInterrupt:
        print("PROGRAM FINISHED by user")
        print("Programm ENDE")


if __name__ == "__main__":
    main()
