import os
import json
import csv

def load_json_from_folder():
    while True:

        try:
            folder_path = input("Enter the folder path where the JSON file is located: ")
            if os.path.isdir(folder_path):
                file_path = os.path.join(folder_path,'vbathula1_adoptions.json')

                if os.path.isfile(file_path):
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                    print("JSON data loaded successfully!")
                    print(data)
                    return data
                else:                   
                    print(f" The file vabthula1_adoptions.json does not exist in the folder '{folder_path}'.")
            else:               
                print(f"The folder '{folder_path}' does not exist.")
        
        except json.JSONDecodeError:
            
            print("Error: The file is not a valid JSON.")
        
        except Exception as e:
            
            print(f"An unexpected error occurred: {e}")


#Function 2 Create 5 CSV Files
#csv1

def save_university_details(data):
    csv_file_name = "university_details.csv"
    
    with open(csv_file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['university_id', 'name', 'address', 'city', 'state', 'zip', 'website'])

        for record in data:
            university = record.get('university', {})
            writer.writerow([
                university.get('id'),
                university.get('name'),
                university.get('address'),
                university.get('city'),
                university.get('state'),
                university.get('zip'),
                university.get('website')
            ])
    
    print(f"University details saved to {csv_file_name}")


#csv2

def save_adoption_information(data):
    csv_file_name = "adoption_information.csv"
    
    with open(csv_file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['adoption_id', 'university_id', 'date', 'quantity', 'book_id'])

        for record in data:
            university_id = record.get('university', {}).get('id')
            adoptions = record.get('adoptions', [])
            for adoption in adoptions:
                writer.writerow([
                    adoption.get('id'),
                    university_id,
                    adoption.get('date'),
                    adoption.get('quantity'),
                    adoption.get('book', {}).get('id')
                ])
    
    print(f"Adoption information saved to {csv_file_name}")

#csv3

def save_book_details(data):
    csv_file_name = "book_details.csv"
    
    with open(csv_file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['book_id', 'isbn10', 'isbn13', 'title', 'category'])

        book_set = set()
        for record in data:
            adoptions = record.get('adoptions', [])
            for adoption in adoptions:
                book = adoption.get('book', {})
                book_id = book.get('id')
                if book_id not in book_set:
                    book_set.add(book_id)
                    writer.writerow([
                        book.get('id'),
                        book.get('isbn10'),
                        book.get('isbn13'),
                        book.get('title'),
                        book.get('category')
                    ])
    
    print(f"Book details saved to {csv_file_name}")


#csv4

def save_contact_information(data):
    csv_file_name = "contact_information.csv"
    
    with open(csv_file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['university_name', 'contact_order', 'gender', 'firstname', 'lastname'])

        for record in data:
            university_name = record.get('university', {}).get('name', 'Unknown University')
            contacts = record.get('contacts', [])
            for contact in contacts:
                writer.writerow([
                    university_name,
                    contact.get('order'),
                    contact.get('gender'),
                    contact.get('firstname'),
                    contact.get('lastname')
                ])
    
    print(f"Contact details saved to {csv_file_name}")



#csv5

def save_messages(data):
    csv_file_name = "messages.csv"
    
    with open(csv_file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['university_name', 'message_id', 'date', 'content', 'category'])

        for record in data:
            university_name = record.get('university', {}).get('name', 'Unknown University')
            messages = record.get('messages', [])
            for message in messages:
                writer.writerow([
                    university_name,
                    message.get('id'),
                    message.get('date'),
                    message.get('content'),
                    message.get('category')
                ])
    
    print(f"Messages saved to {csv_file_name}")



# Call all the individual functions to generate CSV files
def generate_all_csv_files(data):
    
    save_university_details(data)
    save_adoption_information(data)
    save_book_details(data)
    save_contact_information(data)
    save_messages(data)
    print("All CSV files have been generated.")



# Function 5: Display list of universities in a state
def list_universities_by_state(data):
    while True:
        state_name=input('Please enter state name').strip().replace(" ","").lower()
        if not state_name.isalpha():
            print("Invalid input. Please enter a state name with alphabetic characters only (no special characters or numbers).")
            continue
        universities_in_state = []
        for record in data:
            university = record.get('university', {})
            if university.get('state','').replace(" ", "").lower() == state_name:
                universities_in_state.append(university.get('name'))

        if universities_in_state:
            print(f"Universities in {state_name}:")
            for university in universities_in_state:
                print(university)
            break
        else:
            print(f"No universities found in {state_name}.")


# Function 6: List book categories and save titles by category to a text file
def list_books_by_category(data):
    while True:
        categories = set()
        for record in data:
            adoptions = record.get('adoptions', [])
            for adoption in adoptions:
                book_category = adoption.get('book', {}).get('category', 'Unknown')
                categories.add(book_category)

        print("Available book categories:")
        for category in categories:
            print(category)
        
        user_choice = input("Enter the category you want to save book titles for: ").strip().replace(" ","").lower()

        book_titles = []
        for record in data:
            adoptions = record.get('adoptions', [])
            for adoption in adoptions:
                book = adoption.get('book', {})
                if book.get('category','') .replace(" ", "").lower()== user_choice:
                    book_titles.append(book.get('title'))

        if book_titles:
            text_file_name = f"{user_choice}_books.txt".replace(" ", "_")
            with open(text_file_name, 'w') as text_file:
                for title in book_titles:
                    text_file.write(f"{title}\n")
            print(f"Titles of books in the '{user_choice}' category saved to {text_file_name}.")
            break
        else:
            print(f"No books found in the '{user_choice}' category.") 

data = load_json_from_folder()
print('-------------------------')

generate_all_csv_files(data)
print('-------------------------')

list_universities_by_state(data)
print('-------------------------')

list_books_by_category(data)


