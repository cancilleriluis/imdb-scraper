"""
visualizations.py - Create charts from IMDb data

Uses Plotly to create interactive HTML charts.
"""

import pandas as pd
import plotly.express as px


def load_data(filepath="data/processed/imdb_top_movies_detailed.csv"):
    """Load the scraped movie data."""
    df = pd.read_csv(filepath)
    
    # Convert year to integer for analysis
    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    
    # Convert rating to float
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    
    # Create decade column (1990, 2000, 2010, etc.)
    df["decade"] = (df["year"] // 10) * 10
    
    return df


def chart_ratings_distribution(df):
    """
    Create a histogram showing the distribution of ratings.
    """
    fig = px.histogram(
        df,
        x="rating",
        nbins=10,
        title="IMDb Top Movies - Rating Distribution",
        labels={"rating": "IMDb Rating", "count": "Number of Movies"},
        color_discrete_sequence=["#F5C518"]  # IMDb yellow
    )
    
    fig.update_layout(
        template="plotly_dark",
        showlegend=False
    )
    
    fig.write_html("data/processed/chart_ratings.html")
    print("Saved: chart_ratings.html")


def chart_movies_by_decade(df):
    """
    Create a bar chart showing movies count per decade.
    """
    decade_counts = df.groupby("decade").size().reset_index(name="count")
    
    fig = px.bar(
        decade_counts,
        x="decade",
        y="count",
        title="Top Movies by Decade",
        labels={"decade": "Decade", "count": "Number of Movies"},
        color_discrete_sequence=["#F5C518"]
    )
    
    fig.update_layout(template="plotly_dark")
    
    fig.write_html("data/processed/chart_decades.html")
    print("Saved: chart_decades.html")


def chart_top_genres(df):
    """
    Create a bar chart of most common genres.
    """
    # Split genres and count each one
    all_genres = []
    for genres_str in df["genres"].dropna():
        genres_list = [g.strip() for g in genres_str.split(",")]
        all_genres.extend(genres_list)
    
    # Count occurrences
    genre_counts = pd.Series(all_genres).value_counts().head(10)
    
    fig = px.bar(
        x=genre_counts.values,
        y=genre_counts.index,
        orientation="h",
        title="Most Common Genres in Top Movies",
        labels={"x": "Number of Movies", "y": "Genre"},
        color_discrete_sequence=["#F5C518"]
    )
    
    fig.update_layout(
        template="plotly_dark",
        yaxis=dict(autorange="reversed")
    )
    
    fig.write_html("data/processed/chart_genres.html")
    print("Saved: chart_genres.html")


def chart_rating_vs_votes(df):
    """
    Create a scatter plot: Rating vs Number of Votes.
    """
    fig = px.scatter(
        df,
        x="votes",
        y="rating",
        hover_data=["title", "year"],
        title="Rating vs Popularity (Votes)",
        labels={"votes": "Number of Votes", "rating": "IMDb Rating"},
        color_discrete_sequence=["#F5C518"]
    )
    
    fig.update_layout(template="plotly_dark")
    fig.update_traces(marker=dict(size=12))
    
    fig.write_html("data/processed/chart_rating_votes.html")
    print("Saved: chart_rating_votes.html")


def create_all_charts():
    """Generate all visualizations."""
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} movies\n")
    
    print("Creating charts...")
    chart_ratings_distribution(df)
    chart_movies_by_decade(df)
    chart_top_genres(df)
    chart_rating_vs_votes(df)
    
    print("\nAll charts saved to data/processed/")
    print("Open the .html files in your browser to view them!")


if __name__ == "__main__":
    create_all_charts()