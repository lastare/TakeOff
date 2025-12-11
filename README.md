# TakeOff 🚀

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

**TakeOff** is an intelligent Landing Page Analyzer that automates the process of discovering and analyzing high-quality landing page templates. It scrapes demo URLs from popular theme marketplaces (like ThemeWagon) and uses Google's Gemini AI to analyze their structures and components.

## 🌟 Key Features

-   **Automated Web Scraping**: Powered by **Playwright**, it autonomously navigates theme marketplaces to extract live demo URLs.
-   **AI-Powered Analysis**: Integrates with **Google Gemini AI** to inspect landing page content and identify key components (Hero sections, CTAs, Pricing tables, etc.).
-   **Structured Pipeline**: robust workflow that separates scraping and analysis, allowing for scalable data processing.
-   **Modern Architecture**: Built with a clean `src/` layout, strict typing (Mypy), and structured logging (Structlog).
-   **Production Ready**: Includes configuration management via Pydantic and is fully modular.

## 📂 Project Structure

```text
├── scraped_pages/           # Output directory for data
│   ├── templates.txt        # List of scraped demo URLs
│   └── components.txt       # AI Analysis results
├── src/
│   └── takeoff/
│       ├── core/            # Config & Logging
│       ├── utils/
│       │   ├── web_scraper.py # Playwright scraper logic
│       │   └── ai_analyzer.py # Gemini AI integration
│       └── main.py          # Application entry point
├── tests/                   # Pytest suite
├── pyproject.toml           # Project dependencies
├── Makefile                 # Shortcut commands
└── README.md
```

## 🚀 Getting Started

### Prerequisites

-   Python 3.10 or higher
-   [Playwright](https://playwright.dev/) browsers (installed automatically via `playwright install` or `make install`)

### Installation

1. **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd takeoff
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    make install
    # Or manually: pip install -e ".[dev]" && playwright install
    ```

4. **Configuration**:
   Create a `.env` file in the root directory and add your Gemini API Key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## 🛠️ Usage

### Run the Pipeline

To start the full scraping and analysis pipeline:

```bash
# Run the application
python -m takeoff.main

# Run with a limit (helpful for testing)
python -m takeoff.main --limit 3
```

### Outputs

The application will generate two main output files in the `scraped_pages/` directory:

1.  **`templates.txt`**: A raw list of the landing page URLs found during the scraping phase.
2.  **`components.txt`**: The detailed AI analysis of each landing page, describing its sections, style, and purpose.

## ⚙️ Development Commands

We use a `Makefile` to simplify common development tasks.

-   **Run Tests**: `make test`
-   **Lint Code**: `make lint`
-   **Format Code**: `make format`

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
