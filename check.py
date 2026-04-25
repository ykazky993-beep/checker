import requests
import time
import argparse
import json
from datetime import datetime

def normalize(url):
    if not url.startswith("http"):
        return "https://" + url
    return url

def check(url):
    url = normalize(url)

    try:
        start = time.time()
        r = requests.get(url, timeout=5)
        end = time.time()

        result = {
            "url": url,
            "status_code": r.status_code,
            "response_time": round(end - start, 2),
            "time": str(datetime.now()),
            "status": "UP" if r.status_code == 200 else "WEIRD"
        }

        print(f"\n🌐 {url}")
        print(f"📡 {r.status_code}")
        print(f"⚡ {result['response_time']}s")
        print(f"🟢 {result['status']}")

        return result

    except Exception:
        result = {
            "url": url,
            "status_code": None,
            "response_time": None,
            "time": str(datetime.now()),
            "status": "DOWN"
        }

        print(f"\n🔴 {url} DOWN")
        return result

def save_log(data, file="log.json"):
    try:
        with open(file, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(data)

    with open(file, "w") as f:
        json.dump(logs, f, indent=2)

def load_urls(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("targets", nargs="*", help="URL list")
    parser.add_argument("-f", "--file", help="file berisi list URL")
    parser.add_argument("-t", "--time", type=int, help="loop tiap X detik")

    args = parser.parse_args()

    urls = []

    if args.file:
        urls = load_urls(args.file)
    else:
        urls = args.targets

    if not urls:
        print("❌ using URL or file")
        return

    while True:
        for url in urls:
            result = check(url)
            save_log(result)

        if not args.time:
            break

        print(f"\n⏳ wait {args.time} second...\n")
        time.sleep(args.time)

if __name__ == "__main__":
    main()