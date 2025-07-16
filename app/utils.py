import requests
import tempfile
async def download_resource(url: str) -> str | None:
    """
    Downloads a resource from the given URL and returns the file path.
    If the download fails, returns None.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_file.write(response.content)
            temp_file.close()

            return temp_file.name
        else:
            print(f"Failed to download resource. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while downloading the resource: {e}")
        return None 