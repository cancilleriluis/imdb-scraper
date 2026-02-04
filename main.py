"""
main.py - Entry point for IMDb scraper
"""

import pandas as pd
from src.scraper import scrape_top_movies


def main():
    # Scrape movies WITH details (limit to 5 for testing)
    # This will take ~25 seconds because we wait 1 sec between requests
    movies = scrape_top_movies(include_details=True)
    
    # Convert to DataFrame
    df = pd.DataFrame(movies)
    
    # Show preview
    print("\n=== Preview of scraped data ===\n")
    print(df.to_string())  # Show all columns
    
    # Save to CSV
    output_path = "data/processed/imdb_top_movies_detailed.csv"
    df.to_csv(output_path, index=False)
    print(f"\nData saved to {output_path}")


if __name__ == "__main__":
    main()