# Separam functionalitatea de incarcare a cartilor intr-un fisier separat pentru a mentine codul organizat și modular.
def load_books():
    with open("data/book_summaries.md", "r", encoding="utf-8") as f:
        text = f.read() 

    books = text.split("## Title:")
    books = [b.strip() for b in books if b.strip()]
    return books