from data_loader import load_books

BOOKS = load_books()

def get_summary_by_title(searched_title):
    for book in BOOKS:
        lines = book.split("\n", 1)

        if len(lines) < 2:
            continue

        title = lines[0].strip()
        summary = lines[1].strip()

        if title.lower() == searched_title.lower():
            return summary

    return "Book not found."

print(get_summary_by_title("The Hobbit"))