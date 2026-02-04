"""
scraper.py - Main scraping logic for IMDb Top 250

This module handles:
- Fetching the Top 250 list page
- Fetching individual movie pages
- Extracting all movie data
"""

import requests
from bs4 import BeautifulSoup
import re
import time


# Constants
URL = "https://www.imdb.com/chart/top/"
BASE_URL = "https://www.imdb.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def fetch_page(url):
    """
    Fetch a webpage and return BeautifulSoup object.
    
    Args:
        url: The webpage URL to fetch
        
    Returns:
        BeautifulSoup object ready for parsing
    """
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch page. Status code: {response.status_code}")
    
    return BeautifulSoup(response.content, "lxml")


def clean_votes(votes_text):
    """
    Convert votes text like "(3.2M)" to a number.
    
    Examples:
        "(3.2M)" → 3200000
        "(972K)" → 972000
    """
    if not votes_text or votes_text == "N/A":
        return None
    
    cleaned = votes_text.replace("(", "").replace(")", "").strip()
    
    if "M" in cleaned:
        number = float(cleaned.replace("M", "").replace(",", "."))
        return int(number * 1_000_000)
    
    if "K" in cleaned:
        number = float(cleaned.replace("K", "").replace(",", "."))
        return int(number * 1_000)
    
    return int(cleaned.replace(",", "").replace(".", ""))


def clean_title(title_text):
    """
    Remove the ranking number from title.
    
    Example:
        "1. Cadena perpetua" → "Cadena perpetua"
    """
    if not title_text:
        return "N/A"
    
    parts = title_text.split(". ", 1)
    if len(parts) > 1:
        return parts[1]
    return title_text


def extract_movie_link(movie_element):
    """
    Extract the link to the movie's detail page.
    
    Args:
        movie_element: BeautifulSoup element containing one movie
        
    Returns:
        Full URL to movie detail page
    """
    link_tag = movie_element.select_one("a.ipc-title-link-wrapper")
    if link_tag:
        href = link_tag.get("href", "")
        # href is like "/title/tt0111161/?ref_=chttp_t_1"
        # We need full URL: "https://www.imdb.com/title/tt0111161/"
        return BASE_URL + href.split("?")[0]
    return None


def extract_basic_data(movie_element):
    """
    Extract basic data from a movie in the Top 250 list.
    
    This is the data visible on the list page (without visiting the movie page).
    """
    # Title
    title_tag = movie_element.select_one("h3.ipc-title__text")
    raw_title = title_tag.get_text(strip=True) if title_tag else "N/A"
    title = clean_title(raw_title)
    
    # Year
    metadata_items = movie_element.select("span.cli-title-metadata-item")
    year = metadata_items[0].get_text(strip=True) if metadata_items else "N/A"
    
    # Rating
    rating_tag = movie_element.select_one("span.ipc-rating-star--rating")
    rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"
    
    # Votes
    votes_tag = movie_element.select_one("span.ipc-rating-star--voteCount")
    votes_raw = votes_tag.get_text(strip=True) if votes_tag else "N/A"
    votes = clean_votes(votes_raw)
    
    # Image URL
    img_tag = movie_element.select_one("img.ipc-image")
    image_url = img_tag.get("src") if img_tag else "N/A"
    
    # Link to detail page
    detail_url = extract_movie_link(movie_element)
    
    return {
        "title": title,
        "year": year,
        "rating": rating,
        "votes": votes,
        "image_url": image_url,
        "detail_url": detail_url
    }


def extract_movie_details(detail_url):
    """
    Extract detailed info from a movie's individual page.
    
    This gets: genres, duration, director, writers, actors, plot.
    
    Args:
        detail_url: Full URL to the movie's page
        
    Returns:
        Dictionary with detailed movie info
    """
    soup = fetch_page(detail_url)
    
    # GENRES
    genre_chips = soup.select("a.ipc-chip span")
    genres = [chip.get_text(strip=True) for chip in genre_chips]
    
    # DURATION
    runtime = soup.select_one("li[data-testid='title-techspec_runtime']")
    duration = "N/A"
    if runtime:
        raw_text = runtime.get_text(strip=True)
        match = re.search(r'(\d+h\s*\d*m?)', raw_text)
        duration = match.group(1) if match else "N/A"
    
    # DIRECTOR (section 1 in the credits)
    director_links = soup.select("a[href*='tt_ov_1']")
    directors = list(set([link.get_text(strip=True) for link in director_links]))
    
    # WRITERS (section 2)
    writer_links = soup.select("a[href*='tt_ov_2']")
    writers = list(set([link.get_text(strip=True) for link in writer_links]))
    
    # ACTORS (section 3)
    actor_links = soup.select("a[href*='tt_ov_3']")
    actors = list(set([link.get_text(strip=True) for link in actor_links]))
    
    # PLOT
    plot_tag = soup.select_one("span[data-testid='plot-l']")
    plot = plot_tag.get_text(strip=True) if plot_tag else "N/A"
    
    return {
        "genres": ", ".join(genres),  # Convert list to comma-separated string
        "duration": duration,
        "directors": ", ".join(directors),
        "writers": ", ".join(writers),
        "actors": ", ".join(actors),
        "plot": plot
    }


def scrape_top_movies(limit=None, include_details=False):
    """
    Main function: Scrape movies from IMDb Top 250.
    
    Args:
        limit: Max number of movies to scrape (None = all available)
        include_details: If True, visit each movie page for extra info
        
    Returns:
        List of dictionaries with movie data
    """
    print("Fetching IMDb Top 250 list...")
    soup = fetch_page(URL)
    
    movie_elements = soup.select("li.ipc-metadata-list-summary-item")
    print(f"Found {len(movie_elements)} movies on list page")
    
    # Apply limit if specified
    if limit:
        movie_elements = movie_elements[:limit]
        print(f"Limiting to {limit} movies")
    
    movies = []
    total = len(movie_elements)
    
    for i, movie_element in enumerate(movie_elements):
        # Extract basic data from list page
        movie_data = extract_basic_data(movie_element)
        
        # Optionally fetch detailed info from movie page
        if include_details and movie_data["detail_url"]:
            print(f"[{i+1}/{total}] Fetching details for: {movie_data['title']}")
            
            details = extract_movie_details(movie_data["detail_url"])
            movie_data.update(details)  # Merge details into movie_data
            
            # Be polite: wait 1 second between requests to not overload IMDb
            time.sleep(1)
        else:
            print(f"[{i+1}/{total}] {movie_data['title']}")
        
        movies.append(movie_data)
    
    print(f"\nSuccessfully extracted {len(movies)} movies")
    return movies