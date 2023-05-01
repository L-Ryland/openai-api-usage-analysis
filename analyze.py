import requests
from os import getenv
from dotenv import load_dotenv
import pandas as pd
from datetime import date, datetime, timedelta

load_dotenv(".env.local")
token = getenv("OPENAI_API")
headers = {"authorization": "Bearer " + getenv("OPENAI_API")}
user_id = getenv("USER_PUBLIC_ID")
print("token", token)
print("user_id", user_id)


def main():
    start_time, end_time = getenv("START_TIME"), getenv("END_TIME")
    tmp = start_time
    raw = pd.DataFrame()
    while tmp < end_time:
        tmp = datetime.strptime(tmp, "%Y-%m-%d") + timedelta(days=1)
        tmp = date.strftime(tmp, "%Y-%m-%d")
        params = {"date": tmp, "user_public_id": user_id}
        response = requests.get("https://api.openai.com/v1/usage",
                                headers=headers, params=params).json()

        # print(response)
        if response and len(response["data"]) == 0:
            continue
        tmp2 = pd.DataFrame(response["data"])
        tmp2 = tmp2.assign(aggregation_timestamp=lambda x: pd.to_datetime(
            x["aggregation_timestamp"], unit='s'))
        raw = pd.concat([raw, tmp2])
        # print("result", raw)
    raw.reset_index(drop=True).set_index("aggregation_timestamp").to_csv(f"openai-api-usage-{start_time}-{end_time}.csv")
main()