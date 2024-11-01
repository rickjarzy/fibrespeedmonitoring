import time
from cfspeedtest import CloudflareSpeedtest


def run_speedtest() -> None:
    print("run speedtest ...")
    suite = CloudflareSpeedtest()
    results = suite.run_all()
    print(results)

def main() -> None:
    run_speedtest()
    print("Programm ENDE")

if __name__ == "__main__":
    main()