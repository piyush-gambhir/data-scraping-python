from provider_identification import identify_dealer_provider
from dealer_scraping import scrape_ansira, scrape_dealerdotcom, scrape_overfuel, scrape_dealer_car_search, scrape_dealer_inspire, scrape_random


def main(url, custom_sitemap_url, vin_x_path, images_container_x_path):
    try:
        provider = identify_dealer_provider(url)
        print(f"The provider for the website is: {provider}")
        if provider is None:
            print("The provider could not be identified.")
            provider = None
    except Exception as e:
        print(f"Error: {e}")
        provider = None

    try:
        if (provider.lower() == 'ansira'):
            scrape_ansira(url)
        elif (provider.lower() == 'dealer.com'):
            scrape_dealerdotcom(url)
        elif (provider.lower() == 'overfuel'):
            scrape_overfuel(url)
        elif (provider.lower() == 'dealercarsearch'):
            scrape_dealer_car_search(url)
        elif (provider.lower() == 'dealerinspire'):
            scrape_dealer_inspire(url)
        else:
            scrape_random(url,
                          custom_sitemap_url,
                          vin_x_path,
                          images_container_x_path)

        print("Dealer Inventory Scraping Completed")
    except Exception as e:
        print(f"Error: {e}")
        print("Dealer Inventory Scraping Failed")


if __name__ == "__main__":
    website_input_url = 'https://www.saford.com/new-San+Antonio-2023-Ford-F+150-Lariat-1FTFW1E83PKD23356'
    custom_sitemap_url = None
    vin_x_path = None
    images_container_x_path = None
    main(website_input_url, custom_sitemap_url,
         vin_x_path, images_container_x_path)
