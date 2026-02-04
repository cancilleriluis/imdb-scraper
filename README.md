# IMDb Top 250 Scraper

A Python web scraper that extracts movie data from IMDb's Top 250 list.

## What it does

Scrapes the following data for each movie:
- Title
- Release year
- IMDb rating
- Number of votes
- Poster image URL

## Project Structure
```
imdb-scraper/
├── data/
│   ├── raw/           # Raw HTML files (for debugging)
│   └── processed/     # Clean CSV output
├── src/
│   ├── __init__.py
│   └── scraper.py     # Main scraping logic
├── main.py            # Entry point
├── requirements.txt   # Dependencies
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/imdb-scraper.git
cd imdb-scraper
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python3 main.py
```

Output will be saved to `data/processed/imdb_top_movies.csv`

## Example Output

| title | year | rating | votes | image_url |
|-------|------|--------|-------|-----------|
| Cadena perpetua | 1994 | 9.3 | 3200000 | https://... |
| El padrino | 1972 | 9.2 | 2200000 | https://... |

## Tech Stack

- **Python 3**
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP requests
- **Pandas** - Data handling and CSV export

## What I Learned

- Web scraping fundamentals with BeautifulSoup
- CSS selectors for extracting specific HTML elements
- Data cleaning (converting "3.2M" → 3200000)
- Project organization and best practices

## Future Improvements

- [ ] Scrape all 250 movies (currently gets 25)
- [ ] Extract additional details (director, actors, genre)
- [ ] Add data visualizations
- [ ] Download poster images locally

## License

MIT License - feel free to use this code for learning!