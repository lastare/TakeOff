from playwright.sync_api import sync_playwright
import os
from urllib.parse import urlparse
import time


def get_demo_urls_from_themewagon(page_url="https://themewagon.com/theme-category/landing-website/"):
    """
    Go to the ThemeWagon landing page category and extract demo URLs.
    """
    print(f"Extracting demo URLs from {page_url}...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set a realistic user agent
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })
            
            page.goto(page_url, timeout=60000)
            page.wait_for_load_state("networkidle", timeout=30000)

            # Extract hrefs from elements with class 'btn-hover'
            # These are typically the "Live Preview" or "Details" buttons
            links = page.locator('a.btn-hover').evaluate_all("(elements) => elements.map(el => el.href)")
            
            browser.close()
            
            # Deduplicate links just in case
            unique_links = list(set(links))
            
            print(f"Found {len(unique_links)} demo URLs.")
            return unique_links
        except Exception as e:
            print(f"Error extracting demo URLs: {str(e)}")
            return []


def scrape_landing_page(url):
    """
    Scrape the content of a landing page using Playwright and return it as text.
    """
    with sync_playwright() as p:
        try:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Set a realistic user agent
            page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            })

            # Navigate to the page
            page.goto(url, timeout=30000)

            # Wait for the page to load
            page.wait_for_load_state("networkidle", timeout=10000)

            # Get the text content of the page
            content = page.inner_text('body')

            browser.close()

            return content

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return f"Error: Could not scrape content from {url}"


def save_scraped_content(url, output_dir="scraped_pages"):
    """
    Save the scraped content of a URL to a text file.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract domain name for filename
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace('www.', '').replace('.', '_')
    path = parsed_url.path.replace('/', '_').strip('_')

    # Create filename
    if path:
        filename = f"{domain}_{path}.txt"
    else:
        filename = f"{domain}_homepage.txt"

    filepath = os.path.join(output_dir, filename)

    # Scrape content
    content = scrape_landing_page(url)

    # Save to file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(f"URL: {url}\n\n")
        file.write("="*50 + "\n\n")
        file.write(content)

    print(f"Saved content from {url} to {filepath}")
    return filepath


def scrape_demo_urls(output_file="scraped_pages/templates.txt", limit=None):
    """
    Get URLs from themewagon and scrape each landing page into a single file.
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        urls = get_demo_urls_from_themewagon()

        if limit:
            print(f"Limiting scraping to first {limit} URLs")
            urls = urls[:limit]

        # Clear the file first
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("")

        scraped_count = 0
        for i, url in enumerate(urls, 1):
            print(f"Scraping {i}/{len(urls)}: {url}")
            try:
                # We only want to save the URL now
                # content = scrape_landing_page(url) # No longer scraping content
                
                with open(output_file, 'a', encoding='utf-8') as file:
                    file.write(f"{url}\n")
                
                scraped_count += 1
                # Be respectful with requests (reduced sleep since we aren't scraping full pages)
                time.sleep(0.5)
            except Exception as e:
                print(f"Failed to scrape {url}: {str(e)}")

        return scraped_count
    except Exception as e:
        print(f"Critical error in scraper: {e}")
        return 0


if __name__ == "__main__":
    count = scrape_demo_urls(limit=2)
    print(f"\nSuccessfully scraped {count} URLs into scraped_pages/templates.txt.")
