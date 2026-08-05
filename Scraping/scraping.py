import asyncio, os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta
from apify_client import ApifyClientAsync
from apify_client.errors import ApifyApiError, NotFoundError

load_dotenv(r"C:\Users\yovin\Desktop\Car-IA\.venv-1\.env")
token = os.getenv('API_KEY')


async def main() -> None:
    apify_client = ApifyClientAsync(
        token=token,
        max_retries=3,
        min_delay_between_retries=timedelta(milliseconds=500),
        timeout_short=timedelta(seconds=5),
        timeout_medium=timedelta(seconds=30),
        timeout_long=timedelta(seconds=360),
        timeout_max=timedelta(seconds=360),
    )

    actor_client = apify_client.actor('FINDACTOR')
    

    
    # dataset_client = apify_client.dataset('dataset-id')
    # call_result = await actor_client.call()
    try:
    # start the actor and get the run ID

        input_data =  {
                    'zip': 'zip',
                    'maxItems': '',
                    'mileRadius': '',
                    "startUrl": ""
        }

        run_result = await actor_client.start(run_input=input_data ,wait_for_finish=60)
        run_client = apify_client.run(run_result.id)
        log_client = run_client.log()
        dataset_id = run_client.get("defaultDatasetId")

        async with log_client.stream() as async_log_stream:
            if async_log_stream:
                async for bytes_chunk in async_log_stream.aiter_bytes():
                    print(bytes_chunk)


        csv_bytes = apify_client.dataset(dataset_id).download_items(item_format="csv")
        csv_text = csv_bytes.decode('utf-8')


        with open("listings.csv", "w", encoding="utf-8") as f:
            f.write(csv_text)

        print("Car listings were saved successefuly to CSV!")
        
    except NotFoundError:
        print(f"Error Provided: {NotFoundError}")
    except ApifyApiError as err:
        print(f"API Error: {err}")
        pass

if __name__ == '__main__':
    asyncio.run(main())





    