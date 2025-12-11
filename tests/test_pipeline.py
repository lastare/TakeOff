import os
import sys
from unittest.mock import patch
from takeoff.main import main

def test_pipeline_real_scrape_mock_ai(capsys):
    """
    Test the pipeline with REAL scraping (limit 3) but MOCKED AI.
    Verifies that we can hit ThemeWagon and extract 3 URLs.
    """
    # 1. Setup arguments: limit = 3
    test_args = ["takeoff", "--limit", "3"]

    # 2. Mock ONLY the AI Analyzer (we don't want to burn API credits in tests)
    #    We DO NOT mock scrape_demo_urls, so it will actually run and hit ThemeWagon.
    with patch("takeoff.main.LandingPageAnalyzer") as mock_analyzer_cls, \
         patch.object(sys, 'argv', test_args):

        # Setup the mock analyzer to return a dummy success list
        mock_instance = mock_analyzer_cls.return_value
        mock_instance.analyze_scraped_pages.return_value = [
            {'url': 'http://mock-url-1.com', 'status': 'analyzed'},
            {'url': 'http://mock-url-2.com', 'status': 'analyzed'},
            {'url': 'http://mock-url-3.com', 'status': 'analyzed'}
        ]

        # 3. Run the application
        print("\n\n--- RUNNING INTEGRATION TEST (Real Scraper, Mock AI) ---")
        exit_code = main()

        # 4. Assertions
        assert exit_code == 0
        
        # Verify the AI Analyzer was called with limit=3
        mock_instance.analyze_scraped_pages.assert_called_once_with(limit=3)

        # 5. VERIFY OUTPUTS
        # Check that scraped_pages/templates.txt exists and has 3 lines
        output_file = "scraped_pages/templates.txt"
        assert os.path.exists(output_file), "templates.txt was not created!"
        
        with open(output_file, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        
        print(f"Scraped URLs found in file: {lines}")
        
        assert len(lines) == 3, f"Expected 3 URLs in templates.txt, found {len(lines)}"
        
        # Basic validation that they look like URLs
        for url in lines:
            assert url.startswith("http"), f"Invalid URL scraped: {url}"

        # Check stdout for success messages
        captured = capsys.readouterr()
        assert "Successfully scraped 3 pages" in captured.out
