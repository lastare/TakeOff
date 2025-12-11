import sys
import os
import argparse

from takeoff.core.config import settings
from takeoff.core.logging import configure_logger, logger
from takeoff.utils.web_scraper import scrape_demo_urls
from takeoff.utils.ai_analyzer import LandingPageAnalyzer


def main() -> int:
    """
    Main application entry point.
    """
    configure_logger()

    log = logger.bind(task="startup")
    log.info(
        "Starting up application", app_name=settings.APP_NAME, env=settings.APP_ENV
    )

    parser = argparse.ArgumentParser(description="TakeOff Landing Page Analyzer")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of URLs to scrape and analyze")
    args = parser.parse_args()

    try:
        # Application Logic from Reference
        log.info("Starting landing page analysis pipeline...")
        print("Starting landing page analysis pipeline...")

        if args.limit:
            log.info(f"Limit set to {args.limit}")
            print(f"Limit set to {args.limit}")

        # Step 1: Scrape demo URLs to get page content
        log.info("Step 1: Scraping landing pages...")
        print("\nStep 1: Scraping landing pages...")
        
        # Step 1: Browse ThemeWagon to get demo URLs and scrape them
        log.info("Step 1: Scraping landing pages from ThemeWagon...")
        print("\nStep 1: Scraping landing pages from ThemeWagon...")
        
        scraped_count = scrape_demo_urls(limit=args.limit)
        
        log.info(f"Successfully scraped {scraped_count} pages.")
        print(f"\nSuccessfully scraped {scraped_count} pages.")

        # Step 2: Analyze scraped content using AI
        log.info("Step 2: Analyzing landing pages with AI...")
        print("\nStep 2: Analyzing landing pages with AI...")
        
        analyzer = LandingPageAnalyzer()
        results = analyzer.analyze_scraped_pages(limit=args.limit)

        log.info(f"Successfully analyzed {len(results)} pages.")
        print(f"\nSuccessfully analyzed {len(results)} pages.")

        # Summary
        log.info("Pipeline completed! Summary available in console.")
        print("\nPipeline completed! Here's a summary:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['url']}")
            print(f"   Status: {result['status']}")

        print("\nCheck 'scraped_pages/templates.txt' for scraped URLs and 'scraped_pages/components.txt' for analysis results.")

        log.info("Application finished successfully")
        return 0
    except Exception as e:
        log.exception("Application crashed", error=str(e))
        return 1

if __name__ == "__main__":
    sys.exit(main())
