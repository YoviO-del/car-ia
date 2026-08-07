import logging
import asyncio, os
from dotenv import load_dotenv
from datetime import timedelta
from apify_client import ApifyClientAsync
from apify_client.errors import ApifyApiError, NotFoundError

load_dotenv(r"C:\Users\yovin\Desktop\Car-IA\.venv-1\.env")
token = os.getenv('API_KEY')

# Configure the Apify client logger
apify_client_logger = logging.getLogger('apify_client')
apify_client_logger.setLevel(logging.DEBUG)
apify_client_logger.addHandler(logging.StreamHandler())


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

    actor_client = apify_client.actor('harvestapi/linkedin-profile-scraper')
    

    
    # dataset_client = apify_client.dataset('dataset-id')
    # call_result = await actor_client.call()
    try:
    # start the actor and get the run ID

        input_data =  {
            "profileScraperMode": "Profile details no email ($4 per 1k)",
            "queries": [
                "https://www.linkedin.com/in/yapheth-gessesse/"
            ]
        }

        run_result = await actor_client.start(run_input=input_data, wait_for_finish=60)

        run_id = run_result.id  # ✅ Run object, use attribute access
        run_client = apify_client.run(run_id)

        run_data = await run_client.get()
        dataset_id = run_data.default_dataset_id  # ✅ snake_case attribute, not dict key

        log_client = run_client.log()
        async with log_client.stream() as async_log_stream:
            if async_log_stream:
                async for bytes_chunk in async_log_stream.aiter_bytes():
                    print(bytes_chunk)


        csv_bytes = await apify_client.dataset(dataset_id).get_items_as_bytes(item_format="csv")
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





    