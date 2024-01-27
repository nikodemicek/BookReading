import requests
import re 
from bs4 import BeautifulSoup
import openai

from key import get_key()




def get_book_info(list_of_books):
    """
    Returns a list of books with their information
    """
    predicted_books = []
    for book in list_of_books:
        try:
            predicted_book = search_book(book)[0] 
        except (IndexError, TypeError):
            predicted_book =  {}

        if not predicted_book:
            predicted_book["title"] = refine_search_term(book)
            predicted_book["authors"] = []

        # Safely get title and authors, handling the case where they might not be set
        book_title = predicted_book.get("title", "Book not found")
        book_authors = ", ".join(predicted_book.get("authors", []))
        full_title = f"{book_title} {book_authors}"

        if book_title != "Book not found":
            predicted_book["goodreads_avg_rating"], predicted_book["goodreads_rating_count"] = get_goodreads_rating_info(full_title)
            predicted_books.append(predicted_book)
    
    return predicted_books

openai.api_key = get_key()

def refine_search_term(query):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that help identifying books."},
          {"role": "user", "content": f"""
            Given the input: '{query}', please identify what author and book title does the input represent. 
            The query is a text identified from an image of a book spine using OCR, therefore it may contain errors. 
            Don't worry about that, just try to identify the book as best as you can. The query may contain some extra text, 
            like publisher name or a quote from the book, please ignore those and focus solely on the author and the title.
            Let your response be only and only the author and the title, nothing else. If you are unable to guess the book, or if the query is empty or nonsensical,
            return only 'Book not found' and nothing else. It is very important that you return only the author and the title.
            """}]
    )

    # Extracting the response text
    return response.choices[0].message.content

# Your API Key
API_KEY = "AIzaSyB4phIbOx-K6tR34iIPySs8SoNAIcJDQ-A"

def search_book(search_string):
    """
    Returns a list of books matching the search string
    """
    
    # Construct the API URL
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_string}&langRestrict=en&key={API_KEY}"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        book_list = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            book_metadata = {}
            book_metadata["title"] = volume_info.get('title', 'Unknown Title')
            book_metadata["authors"] = volume_info.get('authors', [])
            book_metadata["description"] = volume_info.get('description', 'No Description')
            book_list.append(book_metadata)
        return book_list
    else:
        #print("Error:", response.status_code)
        return None



def get_goodreads_rating_info(book_title):
    """
    Returns the average rating and number of ratings for a book
    """

    search_string = f'{book_title} \"Goodreads\"'
    # Google search URL (this might be subject to change, ensure it's current)
    GOOGLE_SEARCH_URL = "https://www.google.com/search?hl=en&q=" + search_string

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=1'
    }

    response = requests.get(GOOGLE_SEARCH_URL, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all elements with the class 'z3HNkc'
        search_results = soup.find_all(class_='fG8Fp uo4vr')
        
        rating_results = []
        for result in search_results:
            # Use regex to find the rating pattern
            avg_rating_match = re.search(r"Rating: (\d\,\d{1,2})", result.text)
            ratings_count_match = re.search(r"([\d,]+) (?:votes|reviews)", result.text)


            avg_rating = float(avg_rating_match.group(1).replace(",", ".")) if avg_rating_match else None
            ratings_count = int(ratings_count_match.group(1).replace(",", "")) if ratings_count_match else None
            
            if avg_rating and ratings_count:
                rating_results.append((avg_rating, ratings_count))

        if len(rating_results)>0:
            most_likely_rating = max(rating_results, key=lambda x: x[1])
            if most_likely_rating:
                return most_likely_rating
            else:
                return (0, 0)
        else:
            return (0, 0)
    else:
        print("Error:", response.status_code)
        return (0, 0)