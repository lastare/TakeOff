import os
import openai
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables
load_dotenv()


class LandingPageAnalyzer:
    def __init__(self):
        # Configure OpenAI client for OpenRouter
        self.client = openai.OpenAI(
            base_url='https://openrouter.ai/api/v1',
            api_key=os.getenv('OPENROUTER_API_KEY')
        )

        # Set the model to use
        self.model = os.getenv('OPENROUTER_MODEL', 'openai/gpt-3.5-turbo')

    def analyze_page_components(self, page_content, url):
        """
        Analyze the components of a landing page using AI and return formatted components list.
        """
        prompt = f"""
Analyze the following landing page content from the URL: {url}

Identify and list all the components present on this landing page. Components might include:

- Header/Navigation elements
- Hero section
- Call-to-action buttons
- Features/benefits sections
- Testimonials
- Pricing tables
- Contact forms
- Image galleries
- Video embeds
- Social media links
- Footer elements
- Other UI components

Provide the output in this exact format:

- [Component name]: [Brief description]
- [Component name]: [Brief description]
- [Component name]: [Brief description]

List each component on a separate line starting with a dash, followed by the component name, a colon, and a brief description of its content and purpose.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert web developer and designer who can analyze website components thoroughly. Follow the exact output format requested by the user."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error analyzing content from {url}: {str(e)}"

    def analyze_scraped_pages(self, input_file="scraped_pages/templates.txt", output_file="scraped_pages/components.txt", limit=None):
        """
        Read URLs from input_file, scrape their content on-demand, analyze them, and write results to output_file.
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        if not os.path.exists(input_file):
            print(f"Input file {input_file} not found.")
            return []

        # Read the URLs
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]

        if limit:
            print(f"Limiting analysis to first {limit} pages")
            urls = urls[:limit]

        # Clear output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("")

        results = []
        
        # Helper to scrape (moved logic here or import it)
        from .web_scraper import scrape_landing_page

        for i, url in enumerate(urls, 1):
            print(f"Analyzing page {i}/{len(urls)}: {url}...")
            
            try:
                # Scrape content ON DEMAND now
                page_content = scrape_landing_page(url)
                
                # Limit content size for API call
                max_content_length = 100000 
                if len(page_content) > max_content_length:
                    page_content = page_content[:max_content_length]

                # Perform analysis
                analysis_result = self.analyze_page_components(page_content, url)

                # Append analysis to output file
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(f"ANALYSIS FOR: {url}\n")
                    f.write("-" * 50 + "\n")
                    f.write(analysis_result)
                    f.write("\n\n" + "=" * 50 + "\n\n")

                results.append({
                    'url': url,
                    'status': 'analyzed'
                })

                print(f"Completed analysis for {url}")
            except Exception as e:
                 print(f"Error analyzing {url}: {e}")
                 results.append({
                    'url': url,
                    'status': f'error: {e}'
                })

        return results


if __name__ == "__main__":
    # Initialize the analyzer
    analyzer = LandingPageAnalyzer()

    # Analyze all scraped pages
    results = analyzer.analyze_scraped_pages()

    print("\nAnalysis completed!")
    print(f"Analyzed {len(results)} pages into scraped_pages/components.txt")
