def get_vdp_urls_from_sitemap(sitemap_url):
    """
    Fetch all VDP URLs from the sitemap URL.
    This function parses the sitemap and filters out VDP URLs based on specific patterns.
    """
    try:
        # Fetch the sitemap content using Selenium
        sitemap_content = fetch_sitemap_using_selenium(sitemap_url)
        all_urls = parse_sitemap(sitemap_content)

        vdp_urls = []
        for url in all_urls:
            # VDP pages generally have more segments in their URL paths
            url_path_components = urlparse(url).path.split('/')
            if len(url_path_components) > 2 and url_path_components[-1] != '':
                vdp_urls.append(url)
            elif (len(url_path_components) >= 2 and
                  any(char.isdigit() for char in url_path_components[1])):
                vdp_urls.append(url)

        return vdp_urls
    except Exception as e:
        print(f"Error fetching or parsing sitemap: {e}")
        return []