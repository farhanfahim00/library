#By Sami Ul Haq & Farhan Fahim
#sami.haq@stud.th-deg.de
#farhan.taimoor@stud.th-deg.de

#(Library_model is the model library with all the Backend code)

import json
import os

File_name = "library.json"  #Path to the JSON file

#update File name once a new File is selected
def update_file_name(new_file_name):
    global File_name
    File_name = new_file_name

#loading Books
def load_book():
    if not os.path.exists(File_name):
        return []  #Return empty list if the file doesn't exist
    try:
        with open(File_name, "r") as f:
            books = json.load(f)
            return books
    except json.JSONDecodeError:  # Return empty list if there's a JSON decode error
        return []

#saving Books in the json file
def save_books(books):
    with open(File_name, 'w') as f:
        json.dump(books, f, indent=4)


#Adding new Book in the Library
def add_book(title, author, year, status):
    books = load_book()

    #Check if the book already exists by comparing the titles
    for book in books:
        if book["title"].lower() == title.lower():
            if book["status"] == "deleted" or book["status"] == "lent out":  #If the book is marked as deleted
                book["status"] = "available"  #Restore the status to available
                save_books(books)  #Save the updated list to the JSON file
                print(f'Book "{title}" restored to available status.')
                return  #Exit the function, no need to add a new book
            else:
                print(f"Book '{title}' already exists and is not deleted!")
                return  #Don't add the book if it's already in the list and not deleted

    #If the book doesn't exist, append it to the list
    books.append({"title": title, "author": author, "year": int(year), "status": status})
    save_books(books)  #Save the updated list to the JSON file
    print(f'Book "{title}" added successfully with status "{status}".')

#Delete Book from Library
def delete_book_by_title(title):
    books = load_book()
    books_to_delete = [book for book in books if book["title"].lower() == title.lower()] #Checking for Book in the Library

    if books_to_delete:
        book_to_delete = books_to_delete[-1]  #Get the last matched book
        book_to_delete["status"] = "deleted"  #Set status to deleted
        save_books(books)
        print(f'Book titled "{book_to_delete["title"]}" marked as deleted.')
    else:
        print(f"No book found with the title: {title}") #If No book of the Name is Found

#Listing all the Books
def list_books():
    books = load_book()
    for book in books:
        print(f'{book["title"]} by {book["author"]}, {book["year"]} - Status: {book["status"]}')



#Modifying the code to implement large datasets of 1 Million Entries

def generate_large_data(num_entries=1000000):
    data = []
    for i in range(num_entries):
        title = f"Book {i}"
        author = f"Author {chr(65 + (i % 26))}"
        year = random.randint(1800,2100)
        status = random.choice(["available", "lent out", "missing"]) #book can either be available lent out or missing later
        data.append({"title": title, "author": author, "year": year, "status": status})
    return data

def write_large_data_to_json(data, filename="large_library.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# library_main.py (or test_script.py)
from library_model import generate_large_data, write_large_data_to_json

large_data = generate_large_data()
write_large_data_to_json(large_data)
print("Large data written to large_library.json")


#How it Works all the Rules and Regulations
def how_it_works():
    return """
    This program allows you to manage your library by:

1. Adding Book:
   - Requires all 4 fields: Title, Author, Year, and Status.
   - Adds a new book to the library.

2. Delete Book:
   - Only Title is required to delete a book from the library.
   - The status of the book will be marked as "deleted" 
   instead of being fully removed.

3. List Books:
   - Lists all the books in the library.

4. Search Books:
   - Opens a new window where you can search any book in the 
   selected database (.json file).
   - You can search by Title, Author, Year, or Status.
   
5. Lend Out:
   - You can only lend out books that have an "available" status.
   - Books with "deleted" or "missing" status cannot be lent out.
   - Once a book is lent out, it must be added back to the library with all 4 
   fields (Title, Author, Year, Status) to change its status back to "available."

6. Select Library:
   - Allows you to select between different libraries (databases).
   - You can move between libraries easily.

7. Add New Library:
   - Helps you create a new library (new .json file).
   - The new library is added and can be selected for use.
   
Note: The Text Box Updates/Refreshes itself, 
However to LIST BOOKS again delete the Text box completely

Enjoy using our Library Organizer!

Best Regards,  
Farhan Fahim Taimoor and Sami ul Haq
"""

