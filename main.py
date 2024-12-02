import threading, traceback, os, requests, json, random, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the API endpoint's URL and the authorization token
API_URL = os.getenv("API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

print(API_URL)
print(AUTH_TOKEN)

# Validate environment variables
if not API_URL or not AUTH_TOKEN:
    raise ValueError("API_URL or AUTH_TOKEN is not set in the environment variables")

# Shared counter and lock for thread-safe incrementing
api_call_count = 0
counter_lock = threading.Lock()

# Function to make the API call
def call_api():
    global api_call_count

    data = ""
    base_data = {
        "option": random.randint(1, 4),  # Generate random value for each call
        "data": data,
    }
    
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=base_data)
        with counter_lock:
            api_call_count += 1

        print(f"Response: {response.status_code} {response.text}")
    except requests.RequestException:
        print(traceback.format_exc())

# Main function
def main():
    max_threads = os.cpu_count() - 1 or 1  # At least 1 thread
    max_workers = max_threads * 2

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(call_api) for _ in range(100)]  # Number of needed API calls
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Worker error: {e}")

    print(f"Total API calls made: {api_call_count}")
    print(f"Execution completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()