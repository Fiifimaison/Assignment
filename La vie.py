import datetime
import msvcrt  # Import the msvcrt module for Windows
import os

# File to store user credentials
CREDENTIALS_FILE = "credentials.txt"
# File to store user locations
LOCATIONS_FILE = "locations.txt"
# File to store user reservations
RESERVATIONS_FILE = "reservations.txt"

# Dictionary to store user credentials
users = {}
# Dictionary to store user locations
user_locations = {}
# Dictionary to store user reservations
user_reservations = {}

def load_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        # If the file doesn't exist, create an empty one
        with open(CREDENTIALS_FILE, "w"):
            pass

    # Now load the credentials from the file as before
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                users[username] = password
    except FileNotFoundError:
        # If the file doesn't exist, there are no existing credentials
        pass

def save_credentials():
    with open(CREDENTIALS_FILE, "w") as file:
        for username, password in users.items():
            file.write(f"{username},{password}\n")

def load_locations():
    if not os.path.exists(LOCATIONS_FILE):
        # If the file doesn't exist, create an empty one
        with open(LOCATIONS_FILE, "w"):
            pass

    # Now load the locations from the file as before
    try:
        with open(LOCATIONS_FILE, "r") as file:
            for line in file:
                username, location_name, city, country = line.strip().split(",")
                if username not in user_locations:
                    user_locations[username] = []
                user_locations[username].append((location_name, city, country))
    except FileNotFoundError:
        # If the file doesn't exist, there are no existing locations
        pass

def save_locations():
    with open(LOCATIONS_FILE, "w") as file:
        for username, locations in user_locations.items():
            for location_name, city, country in locations:
                file.write(f"{username},{location_name},{city},{country}\n")

def load_reservations():
    if not os.path.exists(RESERVATIONS_FILE):
        # If the file doesn't exist, create an empty one
        with open(RESERVATIONS_FILE, "w"):
            pass

    # Now load the reservations from the file as before
    try:
        with open(RESERVATIONS_FILE, "r") as file:
            for line in file:
                username, location_name, city, country, timestamp_str = line.strip().split(",")
                timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                if username not in user_reservations:
                    user_reservations[username] = []
                user_reservations[username].append((location_name, city, country, timestamp))
    except FileNotFoundError:
        # If the file doesn't exist, there are no existing reservations
        pass

def save_reservations():
    with open(RESERVATIONS_FILE, "w") as file:
        for username, reservations in user_reservations.items():
            for location_name, city, country, timestamp in reservations:
                timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{username},{location_name},{city},{country},{timestamp_str}\n")

def create_account():
    print("-------------- CREATE ACCOUNT ---------------")
    while True:
        username = input("Enter a new username: ")
        if username in users:
            print("Username already exists. Please choose a different username.")
        else:
            break
    
    print("Enter a password: ", end="", flush=True)  # Prompt without newline
    password = ""
    while True:
        char = msvcrt.getch().decode("utf-8")
        if char == "\r" or char == "\n":  # Enter key
            break
        elif char == "\x08":  # Backspace key
            if password:
                password = password[:-1]
                print("\b \b", end="", flush=True)  # Erase the last character
        else:
            password += char
            print("*", end="", flush=True)  # Print asterisk to hide the character
    print()  # Move to the next line
    
    users[username] = password
    save_credentials()  # Save the new credentials to file
    user_locations[username] = []  # Initialize empty list for user's locations
    user_reservations[username] = []  # Initialize empty list for user's reservations
    print("Account created successfully!")
    return username, password

def login():
    print("-------------- LOGIN ---------------")
    while True:
        username = input("Enter your username: ")
        if username not in users:
            print("Invalid username. Please try again.")
            continue
        
        print("Enter your password: ", end="", flush=True)  # Prompt without newline
        password = ""
        while True:
            char = msvcrt.getch().decode("utf-8")
            if char == "\r" or char == "\n":  # Enter key
                break
            elif char == "\x08":  # Backspace key
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)  # Erase the last character
            else:
                password += char
                print("*", end="", flush=True)  # Print asterisk to hide the character
        print()  # Move to the next line

        if users[username] == password:
            print("Welcome to La vie Travel & Tour!")
            return username
        else:
            print("Invalid password. Please try again.")

def add_location(username):
    print("-------------- ADD LOCATION ---------------")
    location_name = input("Enter the name of the new location: ")
    city = input("Enter the city: ")
    country = input("Enter the country: ")
    user_locations[username].append((location_name, city, country))
    save_locations()  # Save the new locations to file
    print(f"Location '{location_name}' added successfully!")

def remove_location(username):
    print("-------------- REMOVE LOCATION ---------------")
    print("Your locations:")
    for idx, (location, city, country) in enumerate(user_locations[username], start=1):
        print(f"{idx}. {location} - {city}, {country}")

    choice = input("Enter the number of the location to remove (or 'back' to return to the menu): ")
    if choice.lower() == 'back':
        return

    try:
        choice = int(choice)
        if 1 <= choice <= len(user_locations[username]):
            removed_location = user_locations[username].pop(choice - 1)
            save_locations()  # Save the updated locations to file
            print(f"Location '{removed_location[0]}' removed successfully.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice. Please enter a number.")

def update_location(username):
    print("-------------- UPDATE LOCATION ---------------")
    print("Your locations:")
    for idx, (location, city, country) in enumerate(user_locations[username], start=1):
        print(f"{idx}. {location} - {city}, {country}")

    choice = input("Enter the number of the location to update (or 'back' to return to the menu): ")
    if choice.lower() == 'back':
        return

    try:
        choice = int(choice)
        if 1 <= choice <= len(user_locations[username]):
            location_name, city, country = user_locations[username][choice - 1]
            new_location_name = input("Enter the new name of the location: ")
            new_city = input("Enter the new city: ")
            new_country = input("Enter the new country: ")
            user_locations[username][choice - 1] = (new_location_name, new_city, new_country)
            save_locations()  # Save the updated locations to file
            print("Location updated successfully.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice. Please enter a number.")

def make_reservation(username):
    print("-------------- MAKE RESERVATION ---------------")
    print("Available locations:")
    for idx, (location, city, country) in enumerate(user_locations[username], start=1):
        print(f"{idx}. {location} - {city}, {country}")

    choice = input("Enter the number of the location to reserve (or 'back' to return to the menu): ")
    if choice.lower() == 'back':
        return

    try:
        choice = int(choice)
        if 1 <= choice <= len(user_locations[username]):
            location_name, city, country = user_locations[username][choice - 1]
            timestamp = datetime.datetime.now()
            print(f"Reservation made for '{location_name}' at {timestamp}.")
            user_reservations[username].append((location_name, city, country, timestamp))
            save_reservations()  # Save the new reservation to file
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice. Please enter a number.")

def save_data():
    save_credentials()
    save_locations()
    save_reservations()

# Main program
def main():
    load_credentials()  # Load existing credentials or create the file if it doesn't exist
    load_locations()    # Load existing locations
    load_reservations() # Load existing reservations

    while True:
        choice = input("Do you have an account? (yes/no): ").lower()

        if choice == 'yes':
            username = login()
            if username is not None:
                break
        elif choice == 'no':
            username, password = create_account()
            login()  # Prompting the user to log in immediately after creating the account
            break
        else:
            print("Invalid choice.")

    # Continue with the rest of your program here
    print(f"Welcome, {username}!")
    print("Current timestamp:", datetime.datetime.now())

    while True:
        print("\n--- MENU ---")
        print("1. Location")
        print("2. Reservation")
        print("3. View Reservations")
        print("4. Save Data")
        print("5. Exit")

        option = input("Choose an option (1-5): ")

        if option == '1':  # Location
            while True:
                print("\n--- LOCATION MENU ---")
                print("1. Add new location")
                print("2. Remove location")
                print("3. Update location")
                print("4. Back")

                location_option = input("Choose an option (1-4): ")

                if location_option == '1':  # Add new location
                    add_location(username)
                elif location_option == '2':  # Remove location
                    remove_location(username)
                elif location_option == '3':  # Update location
                    update_location(username)
                elif location_option == '4':  # Back to main menu
                    break
                else:
                    print("Invalid option.")

        elif option == '2':  # Reservation
            make_reservation(username)

        elif option == '3':  # View Reservations
            print("\n--- YOUR RESERVATIONS ---")
            reservations = user_reservations[username]
            if reservations:
                for idx, (location, city, country, timestamp) in enumerate(reservations, start=1):
                    print(f"{idx}. {location} - {city}, {country} - {timestamp}")
            else:
                print("You have no reservations yet.")

        elif option == '4':  # Save Data
            save_data()
            print("Data saved successfully.")

        elif option == '5':  # Exit
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
