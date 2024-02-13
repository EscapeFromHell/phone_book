from phonebook import PhoneBook


def main() -> None:
    """
    Main function of the phone book application.

    This function initializes the PhoneBook object and
    presents the user with a menu of options to interact with
    the phone book.

    """
    phone_book = PhoneBook("phonebook.txt")

    while True:
        print("1. Display Contacts")
        print("2. Add Contact")
        print("3. Edit Contact")
        print("4. Search Contacts")
        print("5. Quit")
        choice = input("Select an option: ")

        if choice == "1":
            phone_book.process_display_contacts()

        elif choice == "2":
            phone_book.process_add_contact()

        elif choice == "3":
            phone_book.process_edit_contact()

        elif choice == "4":
            phone_book.process_search_contacts()

        elif choice == "5":
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
