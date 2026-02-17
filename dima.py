from seleniumbase import SB
import random
import base64
import requests


# -----------------------------
# Utility Functions
# -----------------------------

def fetch_geo_data(proxy):
    """Retrieve geolocation data using optional proxy."""
    try:
        response = requests.get("http://ip-api.com/json/",  timeout=10)
        return response.json(), False
    except requests.exceptions.RequestException:
        fallback = requests.get("http://ip-api.com/json/").json()
        return fallback, False


def decode_username(encoded_str):
    """Decode a Base64 username string."""
    return base64.b64decode(encoded_str).decode("utf-8")


def click_if_present(driver, selector, timeout=4):
    """Click an element if it exists."""
    if driver.is_element_present(selector):
        driver.cdp.click(selector, timeout=timeout)


def random_delay(min_ms=450, max_ms=800):
    """Generate a random delay in seconds."""
    return random.randint(min_ms, max_ms)


def init_driver_session(url, tz, coords):
    """Initialize a SeleniumBase driver with CDP mode."""
    driver = SB(
        uc=True,
        locale="en",
        ad_block=True,
        chromium_arg='--disable-webgl',
        proxy=False
    )
    return driver, url, tz, coords



# -----------------------------
# Main Script Logic
# -----------------------------

proxy_ip = "127.0.0.1"
proxy_port = "18080"
proxy_string = False  # override to disable proxy

proxy_config = {"http": proxy_string}

geo_info, proxy_string = fetch_geo_data(proxy_config)

latitude = geo_info["lat"]
longitude = geo_info["lon"]
timezone_id = geo_info["timezone"]
language_code = geo_info["countryCode"].lower()

encoded_name = "YnJ1dGFsbGVz"
decoded_name = decode_username(encoded_name)
decoded_name = 'blastdota'
target_url = f"https://www.twitch.tv/{decoded_name}"


# -----------------------------
# Main Loop
# -----------------------------


while True:
    driver, url, tz, coords = init_driver_session(
        target_url,
        timezone_id,
        (latitude, longitude),
        
    )

    with driver as main_driver:
        main_driver.activate_cdp_mode(url, tzone=tz, geoloc=coords)
        main_driver.sleep(2)
        click_if_present(main_driver, 'button:contains("Accept")')
        main_driver.sleep(2)

        main_driver.sleep(12)
        click_if_present(main_driver, 'button:contains("Start Watching")')
        main_driver.sleep(10)
        click_if_present(main_driver, 'button:contains("Accept")')

        if main_driver.is_element_present("#live-channel-stream-information"):

            click_if_present(main_driver, 'button:contains("Accept")')

            secondary = main_driver.get_new_driver(undetectable=True)
            secondary.activate_cdp_mode(url, tzone=tz, geoloc=coords)
            secondary.sleep(10)

            click_if_present(secondary, 'button:contains("Start Watching")')
            secondary.sleep(10)
            click_if_present(secondary, 'button:contains("Accept")')

            main_driver.sleep(random_delay())

        else:
            break

