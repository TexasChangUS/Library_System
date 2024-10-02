from shutil import register_unpack_format
from datetime import datetime, timedelta

class Author:
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year
        self.books = set()

    def add_book(self, book):
        self.books.add(book)

class Book:
    def __init__(self, isbn, title, author, year, copies, genre):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies
        self.available_copies = copies
        self.genre = genre

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Author: {self.author}\n"
                f"Year: {self.year}\n"
                f"ISBN: {self.isbn}\n"
                f"Genre: {self.isbn}\n"
                f"Copies: {self.copies}\n"
                f"Available Copies: {self.available_copies}")
    
class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.borrowed_books = {}

    def borrow_book(self, book):
      if book.available_copies > 0:
          self.borrowed_books.append(book)
          book.available_copies -= 1
          print(f"{self.name} borrowed {book.title}")
      else:
          print(f"{book.title} unavailable.")


    def return_book(self, book):
      if book in self.borrowed_books:
        self.borrowed_books.remove(book)
        book.available_copies += 1
        print(f"{self.name} returned {book.title}")
      else:
        print(f"{self.name} hasn't borrowed {book.title}")

    def get_borrowed_books(self):
      if self.borrowed_books:
        return [book.title for book in self.borrowed_books]
      else:
        return f"{self.name} has no titles."
      
class LibraryManagementSystem:
    def __init__(self):
        self.books = {}  # Dictionary: ISBN -> Book object
        self.authors = {}  # Dictionary: name -> Author object
        self.customers = {}  # Dictionary: customerID -> Customer object
        self.genre_classification = {}  # Dictionary: Genre -> {set of ISBNs}
        self.waitlist = {}  # Dictionary: ISBN -> [list of customerIDs]

    def add_book(self, isbn, title, author_name, author_birth_year, year, copies, genre):
      if isbn in self.books:
        print(f"Book with ISBN: {isbn} already present.")
        return

      if author_name not in self.authors:
        self.authors[author_name] = Author(author_name, author_birth_year)

      author = self.authors[author_name]
      book = Book(isbn, title, author, year, copies, genre)
      self.authors[author_name].add_book(book)
      self.books[isbn] = book

      if genre not in self.genre_classification:
        self.genre_classification[genre] = set()
      self.genre_classification[genre].add(isbn)

      print(f"Added book '{title}' by {author_name} to the library ")

    def register_customer(self, name, email):
      customer_id = len(self.customers) + 1
      customer = Customer(customer_id, name, email)
      self.customers[customer_id] = customer

      print(f"Customer '{name}' has been registered with ID: {customer_id}.")
      return customer_id

    def borrow_book(self, isbn, customer_id):
        if isbn not in self.books:
          print("Book unavailable or non-existent.")
          return

        if customer_id not in self.customers:
          print(f"Customer ID: {customer_id} is unavailable or non-existent")
          return

        book = self.books[isbn]
        customer = self.customers[customer_id]

        if book.available_copies <= 0:
          print(f"'{book.title}' is unavailable, all copies are borrowed.")
          return

        customer.borrow_book(book)
        print(f"Borrowed '{book.title}' by {book.author.name} for customer ID: {customer_id}.")

    def return_book(self, isbn, customer_id):
      if isbn not in self.books:
        print("Book unavalable or non-existent.")
        return
      if customer_id not in self.customers:
        print(f"Customer ID: {customer_id} is unavailable or non-existent.")
        return

      book = self.books[isbn]
      customer = self.customers[customer_id]
      customer.return_book(book)

    def search_books(self, query):
      results = []
      for book in self.books.values():
        if (query.lower() in book.title.lower() or query.lower() in book.author.name.lower() or query == book.isbn):
          results.append(book)
        if results:
          for book in results:
            print(book)
        else:
          print("No books found for the given query")

    def display_available_books(self):
      for book in self.books.values():
        if book.available_copies > 0:
          print(book)

    def display_customer_books(self, customer_id):
      if customer_id in self.customers:
        customer = self.customers[customer_id]
        borrowed_books = customer.get_borrowd_books()
        if borrowed_books:
          for book in borrowed_books:
            print(book)
        else:
          print(f"Customer ID: {customer_id} has no borrowed books.")
      else:
        print(f"Customer ID: {customer_id} is unavailable or non-existent.")


    def recommend_books(self, customer_id):
      if customer_id not in self.customers:
        print(f"Customer ID: {customer_id} is not found.")
        return
      customer = self.customers[customer_id]
      genres = {}
      for book in customer.borrowed_books:
        genres[book.genre] = genres.get(book.genre, 0) + 1
      if genres:
        recommended_genre = max(genres, key = genres.get)
        recommended_books = [book for book in self.books.values() if book.genre == recommended_genre and book.available_copies > 0]
        if recommended_books:
          print(f"Recommended books for you in {recommended_genre} :")
          for book in recommended_books:
            print(book)
        else:
          print("No available books to recommend.")
      else:
        print("No genres found in recommendations.")

    def add_to_waitlist(self, isbn, customer_id):
       if isbn not in self.books:
          print(f"Book with ISBN: {isbn} does not exist.")
          return

       if customer_id not in self.customers:
          print(f"Customer ID: {customer_id} is unavailable or non-existent.")
          return

       if isbn not in self.waitlist:
          self.waitlist[isbn] = []

       self.waitlist[isbn].append(customer_id)
       print(f"Customer ID: {customer_id} has been added to the waitlist for Title: {self.books[isbn].title}.")

    def check_late_returns(self, days_threshold=14):
      late_returns = []
      current_date = datetime.now()
      for customer in self.customers.values():
        for book, borrow_date in customer.borrowed_books.items():
          if (current_date - borrow_date).days > days_threshold:
            late_returns.append((customer, book))

      if late_returns:
        print("Late Returns:")
        for customer, book, overdue_days in late_returns:
          print(f"Customer: {customer.name}, Book: {book.title}, Overdue Days: {overdue_days}")
      else:
        print("No late returns found.")

    def run(self):
      while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. Register Customer")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Display Available Books")
        print("6. Display Customer Borrowed Books")
        print("7. Search Books")
        print("8. Add to Waitlist")
        print("9. Exit")
        choice = input("Please select an option (1-9): ")

        if choice == '1':
          isbn = input("Enter ISBN: ")
          title = input("Enter book title: ")
          author_name = input("Enter author name: ")
          author_birth_year = int(input("Enter author birth year: "))
          year = int(input("Enter publication year: "))
          copies = int(input("Enter number of copies: "))
          genre = input("Enter genre: ")
          self.add_book(isbn, title, author_name, author_birth_year, year, copies, genre)

        elif choice == '2':
          name = input("Enter customer name: ")
          email = input("Enter customer email: ")
          self.register_customer(name, email)

        elif choice == '3':
          isbn = input("Enter ISBN of the book to borrow: ")
          customer_id = int(input("Enter customer ID: "))
          self.borrow_book(isbn, customer_id)

        elif choice == '4':
          isbn = input("Enter ISBN of the book to return: ")
          customer_id = int(input("Enter customer ID: "))
          self.return_book(isbn, customer_id)

        elif choice == '5':
          print("\nAvailable Books:")
          self.display_available_books()

        elif choice == '6':
          customer_id = int(input("Enter customer ID: "))
          print(f"\nBooks borrowed by Customer ID {customer_id}:")
          self.display_customer_books(customer_id)

        elif choice == '7':
          query = input("Enter search query (title, author, or ISBN): ")
          print("\nSearch Results:")
          self.search_books(query)

        elif choice == '8':
          isbn = input("Enter ISBN of the book to be waitlisted for: ")
          customer_id = int(input("Enter customer ID: "))
          self.add_to_waitlist(isbn, customer_id)

        elif choice == '9':
          print("Exiting the menu.")
          break

        else:
          print("Invalid, Try again.")

if __name__ == "__main__":
    library = LibraryManagementSystem()
    library.run()
