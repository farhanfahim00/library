#By Sami Ul Haq & Farhan Fahim
#sami.haq@stud.th-deg.de
#farhan.taimoor@stud.th-deg.de

#(Library_main is the main library with the GUIs and the whole Frontend)

#All Imports!
import os
import json
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from library_model import add_book, delete_book_by_title, load_book, save_books, update_file_name, how_it_works
#from library_image import open_image_drawer
from library_image import perform_ocr_batch
from memory_profiler import profile

#Main Window for Library Organizer
window = tk.Tk()
window.geometry("650x650")
window.title("Library Organizer")

selected_library = tk.StringVar(window)

# Main Window Header Label
label = tk.Label(window, text="Welcome to Library Organizer! By Sami-ul-Haq and Farhan Fahim", font=("Arial", 16))
label.grid(row=0, column=0, columnspan=3, pady=10)  # Title of the window spanning 3 columns

#How it Works Function for Rules
def open_how_it_works_window():
    how_it_works_window = tk.Toplevel(window)
    how_it_works_window.title("How it Works")
    how_it_works_window.geometry("500x700")

    rules_text = how_it_works()  #All rules/tutorial are in the Backend Library_model.py

    rules_label = tk.Label(how_it_works_window, text=rules_text, justify=tk.LEFT, padx=10, pady=10)
    rules_label.pack(fill=tk.BOTH, expand=True)

#How it Works Button
how_it_works_button = tk.Button(window, text="How it Works", command=open_how_it_works_window)
how_it_works_button.grid(row=1, column=0, columnspan=3, pady=10)  # Placed after header


# Text box for displaying Book with status
text_area = tk.Text(window, height=10, width=50)
text_area.grid(row=2, column=0, columnspan=3, pady=10)  # Text area in row 1, spanning across 3 columns

# Entry fields for Title, Author, Year, and Status
title_label = tk.Label(window, text="Title:")
title_label.grid(row=3, column=0, pady=5, sticky="e")  # Align label to the right (east)

title_entry = tk.Entry(window, width=40)
title_entry.grid(row=3, column=1, pady=5)

author_label = tk.Label(window, text="Author:")
author_label.grid(row=4, column=0, pady=5, sticky="e")

author_entry = tk.Entry(window, width=40)
author_entry.grid(row=4, column=1, pady=5)

year_label = tk.Label(window, text="Year:")
year_label.grid(row=5, column=0, pady=5, sticky="e")

year_entry = tk.Entry(window, width=40)
year_entry.grid(row=5, column=1, pady=5)

#Dropdown menu for Status (available, lend out, missing, deleted)
status_label = tk.Label(window, text="Status:")
status_label.grid(row=6, column=0, pady=5, sticky="e")

status_var = tk.StringVar(window)
status_var.set("available")  # Default value for status Available

status_options = ["available", "lent out", "missing", "deleted"]
status_menu = tk.OptionMenu(window, status_var, *status_options)
status_menu.grid(row=6, column=1, pady=5)

#All Gui's

#Function to Display books in the Text box
def display_books():
    book_count = 0
    books = load_book()
    text_area.delete(1.0, tk.END)  # Clear text area before displaying books

    if not books:
        text_area.insert(tk.END, "No books in library.")
    else:
        for book in books:
            book_count += 1
            text_area.insert(tk.END,
                             f'{book_count}) {book["title"]} by {book["author"]}, {book["year"]} - Status: {book["status"]}\n')  # List each book
        text_area.insert(tk.END,
                         f'Total Books in the Library ={book_count}')

# Add book Function
def add_book_gui():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()
    status = status_var.get()

    if title and author and year and status:  #Only works If all fields are filled
        books = load_book()  #Load current list of books
        book_found = False

        #Check if the book already exists
        for book in books:
            if book["title"].lower() == title.lower():
                if book["status"] == "deleted" or book["status"] == "lent out":
                    book["status"] = "available"  # Change status to available
                    save_books(books)  # Save the updated list
                    print(f'Book "{title}" restored to available status.')
                    display_books()  # Refresh the book list
                    book_found = True
                    break
                else:
                    print(f"Book '{title}' already exists and is not deleted!")
                    book_found = True
                    break

        if not book_found:  #If the book was not found, add a new book
            add_book(title, author, year, status)
            display_books() #Refresh the list of books
    else:
        print("Please fill in all fields.") #Inform the user if any field is empty

#Delete book function Using Title only
def delete_book_gui():
    title = title_entry.get()  #Get the Title from the title_entry field

    # Check if the title field is filled
    if title:
        # Delete the book by title (Code in Backend Library_model.py)
        delete_book_by_title(title)
        display_books()  #Refresh the book list after deletion
    else:
        print("Please enter a title to delete a book.")


#Search books function
def search_books_gui():
    #Create a new Window for search
    search_window = tk.Toplevel(window)
    search_window.title("Search Books")
    search_window.geometry("700x600")

    #Input fields for search criteria (give any one or all)
    tk.Label(search_window, text="Search by Title:").pack(pady=5)
    title_entry = tk.Entry(search_window, width=40)
    title_entry.pack(pady=5)

    tk.Label(search_window, text="Search by Author:").pack(pady=5)
    author_entry = tk.Entry(search_window, width=40)
    author_entry.pack(pady=5)

    tk.Label(search_window, text="Search by Year:").pack(pady=5)
    year_entry = tk.Entry(search_window, width=40)
    year_entry.pack(pady=5)

    tk.Label(search_window, text="Filter by Status:").pack(pady=5)
    status_var = tk.StringVar(search_window)
    status_var.set("All")  #Default value (can change it into any status)
    status_options = ["All", "available", "lent out", "missing", "deleted"]
    tk.OptionMenu(search_window, status_var, *status_options).pack(pady=5)

    #Treeview for displaying search results
    tree = ttk.Treeview(search_window, columns=("Title", "Author", "Year", "Status"), show="headings")
    tree.heading("Title", text="Title")
    tree.heading("Author", text="Author")
    tree.heading("Year", text="Year")
    tree.heading("Status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    def perform_search():
        #Clear previous results
        for row in tree.get_children():
            tree.delete(row)

        #Get search criteria
        title = title_entry.get().lower()
        author = author_entry.get().lower()
        year = year_entry.get()
        status = status_var.get()

        #Load books and filter
        books = load_book()
        for book in books:
            if (not title or title in book["title"].lower()) and (not author or author in book["author"].lower()) and (not year or str(book["year"]) == year) and (status == "All" or book["status"] == status):
                tree.insert("", tk.END, values=(book["title"], book["author"], book["year"], book["status"]))

    #Search button
    tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)

#Lend book function
def lend_book_gui():
    title = title_entry.get()  #Get the title from the title_entry field

    #Check if the title field is filled
    if title:
        books = load_book()
        book_found = False

        for book in books:
            if book["title"].lower() == title.lower():
                #If the book is available, change its status to 'lent out', if its deleted can't lend it.
                if book["status"] == "available":
                    book["status"] = "lent out"
                    save_books(books)
                    print(f"Book '{title}' has been lent out.")
                    display_books()  #Refresh the book list after lending out
                    book_found = True
                    break
                else:
                    print(f"Book '{title}' is not available to lend out (status: {book['status']}).") #If Book status is deleted or missing
                    book_found = True
                    break

        if not book_found:
            print(f"No book found with the title '{title}'.")
    else:
        print("Please enter a title to lend out a book.")

#Populate book library
def populate_library_list():
    libraries = [file for file in os.listdir() if file.endswith(".json")]
    if not libraries:
        libraries.append("library.json")  #Default library if none exists
        with open("library.json", "w") as f:
            json.dump([], f)
    library_combobox["values"] = libraries
    selected_library.set(libraries[0])
    update_file_name(selected_library.get())

@profile
#Add New Library
def add_new_library():
    add_library_window = tk.Toplevel(window)
    add_library_window.title("Add New Library")
    add_library_window.geometry("300x200")

    tk.Label(add_library_window, text="Enter Library Name:").pack(pady=5)
    new_library_name_entry = tk.Entry(add_library_window, width=30)
    new_library_name_entry.pack(pady=5)

    #Create a New Library
    def create_library():
        new_library_name = new_library_name_entry.get().strip()
        if new_library_name:
            if not new_library_name.endswith(".json"):
                new_library_name += ".json"
            if os.path.exists(new_library_name): #Checking if library already exist in the enviroment
                messagebox.showwarning("Library Exists", "A library with this name already exists.")
            else:
                with open(new_library_name, "w") as f:
                    json.dump([], f)  #Create an empty JSON file
                messagebox.showinfo("Library Created", f"New library created: {new_library_name}")
                populate_library_list()  #Refresh the library list
                add_library_window.destroy()
        else:
            messagebox.showwarning("Invalid Name", "Please enter a valid library name.")

    tk.Button(add_library_window, text="Create Library", command=create_library).pack(pady=10)

# Buttons for Add, Delete, List Books, Lend Out, and Search Books arranged horizontally on row 7
button_frame = tk.Frame(window)
button_frame.grid(row=7, column=0, columnspan=3, pady=10, sticky="ew")

add_button = tk.Button(button_frame, text="Add Book", command=lambda: add_book_gui())
add_button.grid(row=0, column=0, padx=10, sticky="ew")

delete_button = tk.Button(button_frame, text="Delete Book", command=lambda: delete_book_gui())
delete_button.grid(row=0, column=1, padx=10, sticky="ew")

list_button = tk.Button(button_frame, text="List Books", command=lambda: display_books())
list_button.grid(row=0, column=2, padx=10, sticky="ew")

search_button = tk.Button(button_frame, text="Search Books", command=search_books_gui)
search_button.grid(row=0, column=3, padx=10, sticky="ew")

lend_button = tk.Button(button_frame, text="Lend Out", command=lambda: lend_book_gui())
lend_button.grid(row=0, column=4, padx=10, sticky="ew")

#Ensuring the columns are equally distributed by configuring weight and equally distributed
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(3, weight=1)
button_frame.grid_columnconfigure(4, weight=1)

# Library selection dropdown
tk.Label(window, text="Select Library:").grid(row=8, column=0, pady=5)
library_combobox = ttk.Combobox(window, textvariable=selected_library, state="readonly", width=40)
library_combobox.grid(row=8, column=1, pady=5)

# Button for creating a new library
addlibrary_button = tk.Button(window, text="Add new Library", command=add_new_library)
addlibrary_button.grid(row=9, column=0, columnspan=2, pady=10)

# Button for Image Uploading
#upload_image_button = tk.Button(window, text="Upload Image", command=lambda: open_image_drawer(window))
#upload_image_button.grid(row=10, column=0, columnspan=3, pady=10)

#@profile
def extract_text_automatically():
    image_folder = "ocr_images"
    image_files = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
    ]

    extracted_all_text = ""
    if image_files:
        ocr_results = perform_ocr_batch(image_files)
        for image, text in ocr_results.items():
            extracted_all_text += f"---Text from {image}---\n{text}\n\n"
        if extracted_all_text:
            messagebox.showinfo("Extracted Text", extracted_all_text)
        else:
            messagebox.showinfo("Extracted Text", "No text found in any of the images.")
    else:
        messagebox.showinfo("Error", f"No images found in {image_folder}")

#Button for extarcting text automatically
extracttext_button = tk.Button(window,text="Extract Text Automatically", command=extract_text_automatically)
extracttext_button.grid(row=10, column = 0, columnspan=3, pady=3)


#Populate the library list at startup
def populate_combobox():
    populate_library_list()  #Populate the combobox with available libraries
    selected_library.set(library_combobox.get())  #Set default library to the first one

populate_combobox()

#Bind the combobox selection to update the file name
def on_library_selected(event):
    selected_file = selected_library.get()
    update_file_name(selected_file)

library_combobox.bind("<<ComboboxSelected>>", on_library_selected)


extract_text_automatically()




# Start the Tkinter window
window.mainloop()