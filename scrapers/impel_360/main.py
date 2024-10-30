import re
import aiohttp
import asyncio
import json
from pathlib import Path

from utils.logger.setup import setup_logger
from utils.playwright.browser import launch_browser_async
from utils.playwright.navigation import visit_url_async
from utils.json.write import write_json

logger = setup_logger(__name__)


async def find_stock_info(soup):
    stock_span = soup.find("span", class_="stock")
    if stock_span:
        logger.info("Stock info found")
        return stock_span.text.strip().replace("Stock: ", "")
    logger.warning("Stock info not found")
    return None


async def fetch_json(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            logger.error(f"Failed to get JSON data from {url}")
            return None
        logger.info(f"Successfully fetched JSON data from {url}")
        return await response.json()


async def fetch_image_status(session, url):
    async with session.head(url) as response:
        logger.debug(f"Image status for {url}: {response.status}")
        return response.status


async def parse_json(session, cdn_image_prefix, mis_image_count, pano_array):
    exterior, closeups, interior = [], [], []

    # exterior images
    for i in range(100):  # Set a reasonable upper limit
        image_url = f"{cdn_image_prefix}ec/0-{i}.jpg"
        status = await fetch_image_status(session, image_url)
        if status != 200:
            break
        exterior.append(image_url)

    # closeup images
    closeups = [
        f"{cdn_image_prefix}closeups/cu-{i}.jpg" for i in range(mis_image_count)
    ]

    # interior images
    interior = [f"{cdn_image_prefix}pano/pano_{i}.jpg" for i in pano_array]

    logger.info(
        f"Parsed JSON: {len(exterior)} exterior, {len(closeups)} closeups, {len(interior)} interior images"
    )
    return exterior, closeups, interior


async def find_element_by_xpath(page, xpath, attribute, timeout=10):
    try:
        element = await page.wait_for_selector(xpath, timeout=timeout * 1000)
        if element:
            return await element.get_attribute(attribute)
    except Exception as e:
        logger.debug(f"Element not found: {xpath}. Error: {e}")
    return None


async def find_iframe_or_object(page) -> str:
    elements = [
        {
            "xpath": "//iframe[contains(@src, 'embed.spincar')]",
            "attribute": "src"
        },
        {
            "xpath": "//iframe[contains(@src, 'cdn.impel.io') and contains(@src, 'customer=') and contains(@src, 'vin=')]",
            "attribute": "src"
        },
        {
            "xpath": "//iframe[contains(@src, 'spincar-static') and contains(@src, 'customer=') and contains(@src, 'vin=')]",
            "attribute": "src"
        },
        {
            "xpath": "//object[contains(@data, 'spincar.com') and contains(@data, 'customer=') and contains(@data, 'vin=')]",
            "attribute": "data"
        },
    ]
    for element in elements:
        timeout = element.get('timeout', 10)
        result = await find_element_by_xpath(page, element['xpath'], element['attribute'], timeout=timeout)
        if result:
            logger.info(f"Found iframe/object: {result}")
            return result
    logger.warning("No iframe or object found")
    raise Exception("No iframe or object found for the given URL")


async def scrape_360_images(page, vin_no):
    iframe_data = await find_iframe_or_object(page)
    if not iframe_data:
        logger.error("Unable to find iframe_url")
        return None

    patterns = [
        (r"customer=([^!]+)!vin=([^!]+)", False),
        (r"https://spins\.spincar\.com/([^/]+)/([^!]+)", False),
        (r"https://embed\.spincar\.com/spinbuilder/\?vid=([^#]+)", True),
    ]

    for pattern, use_new_format in patterns:
        match = re.search(pattern, iframe_data)
        if match:
            if use_new_format:
                spindef_id = match.group(1)
                base_url = f"https://cdn.impel.io/spindef/{spindef_id}/latest.json"
            else:
                customer, vin = match.groups()
                base_url = f"https://cdn.impel.io/spincar-static/fallback/vinifier/{customer}/{vin}.json"
            break
    else:
        logger.error("No match for json found in iframe_url.")
        return None

    async with aiohttp.ClientSession() as session:
        data = await fetch_json(session, base_url)
        if not data:
            return None

        if use_new_format:
            exterior = data.get("img", {}).get("ec", [])
            closeups = data.get("img", {}).get("cu", [])
            interior = data.get("img", {}).get("i", [])
        else:
            cdn_image_prefix = "https:" + data.get("cdn_image_prefix", "")
            if not cdn_image_prefix:
                logger.error("Failed to get cdn_image_prefix from JSON data")
                return None

            pano_array = ["l", "b", "f", "u", "d", "r"]
            mis_image_count = data["info"]["options"]["numImgCloseup"]
            exterior, closeups, interior = await parse_json(
                session, cdn_image_prefix, mis_image_count, pano_array
            )

        json_data = {
            "vin": data.get("vid", vin_no),
            "vin_no": vin_no,
            "focus_shots": closeups,
            "360_exterior": exterior,
            "360_interior": interior,
        }

        if any([exterior, closeups, interior]):
            json_data["status"] = "success"
            logger.info(f"Successfully scraped 360 images for VIN {vin_no}")
        else:
            json_data["status"] = "failed"
            json_data["error"] = "Error in fetching 360 images"
            logger.error(f"Failed to scrape 360 images for VIN {vin_no}")

        return json_data


async def main():
    try:
        browser, playwright = await launch_browser_async(
            headless=False, browser_type="firefox"
        )
        page = await visit_url_async(
            browser, "https://www.mikeyoung.com/VehicleDetails/certified-2022-Buick-Encore_GX-Preferred-FRANKENMUTH-MI/5894389150"
        )
        vin_no = "5NPE34AFXHH508286"
        result = await scrape_360_images(page, vin_no)

        if result:
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / f"{vin_no}_360_images.json"
            write_json(output_file, result)
            logger.info(f"Results written to {output_file}")
        else:
            logger.error("No results to write")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    finally:
        await browser.close()
        await playwright.stop()


if __name__ == "__main__":
    asyncio.run(main())
