import pandas as pd
import sqlite3
import sys
from pathlib import Path

def get_database_path():
    """Get database path from command line argument or exit if not provided."""
    if len(sys.argv) != 2:
        print("Usage: ./exporter.py <path_to_KoboReader.sqlite>")
        sys.exit(1)
    
    db_path = Path(sys.argv[1])
    if not db_path.exists():
        print(f"Error: Database file '{db_path}' not found")
        sys.exit(1)
        
    return db_path

def get_available_books(conn):
    """Retrieve and display available books from the database."""
    df = pd.read_sql_query("SELECT DISTINCT VolumeID FROM Bookmark", conn)
    books = df["VolumeID"].tolist()
    
    print("\nAvailable books:")
    for idx, book in enumerate(books, 1):
        # Extract just the filename from the path for cleaner display
        book_name = Path(book.replace("file:///mnt/onboard/", "")).name
        print(f"{idx}. {book_name}")
    
    return books

def get_user_choice(books):
    """Get user's book selection."""
    while True:
        try:
            choice = int(input("\nEnter the number of the book to export (or 0 to exit): "))
            if choice == 0:
                sys.exit(0)
            if 1 <= choice <= len(books):
                return books[choice - 1]
            print(f"Please enter a number between 1 and {len(books)}")
        except ValueError:
            print("Please enter a valid number")

def export_annotations(conn, book_id):
    """Export annotations for the selected book."""
    # Get annotations and sort by date
    query = "SELECT Text, DateCreated FROM Bookmark WHERE VolumeID = ?"
    df = pd.read_sql_query(query, conn, params=[book_id])
    
    if df.empty:
        print("No annotations found for this book")
        return
    
    # Sort and prepare for export
    df = df.sort_values(by="DateCreated")
    df.reset_index(inplace=True)

    # Create the output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Create export filename from book ID
    book_name = Path(book_id.replace("file:///mnt/onboard/", "")).stem
    export_filename = output_dir / f"{book_name}_annotations.csv"
    
    # Export to CSV
    df["Text"].to_csv(export_filename, index=True)
    print(f"\nExported {len(df)} annotations to '{export_filename}'")

def main():
    db_path = get_database_path()
    
    try:
        conn = sqlite3.connect(db_path)
        books = get_available_books(conn)
        
        if not books:
            print("No books with annotations found in the database")
            sys.exit(1)
            
        selected_book = get_user_choice(books)
        export_annotations(conn, selected_book)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()