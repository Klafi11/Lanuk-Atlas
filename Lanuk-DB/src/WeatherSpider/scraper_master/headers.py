import random
from config import Settings

Settings = Settings()


def get_random_headers():
    """
    Generiert zufällige Überschriften für Web scraping
    
    Returns:
        dict: Dict der Überschriften
    """
    headers = {
        "User-Agent": random.choice(Settings.USER_AGENTS),
        "Accept": random.choice(Settings.ADDITIONAL_HEADERS["Accept"]),
        "Accept-Language": random.choice(Settings.ADDITIONAL_HEADERS["Accept-Language"]),
        "Accept-Encoding": random.choice(Settings.ADDITIONAL_HEADERS["Accept-Encoding"]),
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    return headers

# Example usage
def example_scraping():
    headers = get_random_headers()
    return headers
