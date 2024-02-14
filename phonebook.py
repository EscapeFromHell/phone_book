import copy
import os

from schemas import Contact as ContactPydantic


class Contact:
    """Represents a contact in the phonebook."""

    def __init__(
        self,
        contact_id: int,
        last_name: str,
        first_name: str,
        middle_name: str,
        organization: str,
        work_phone: str,
        personal_phone: str,
    ) -> None:
        self.contact_id = contact_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone


class PhoneBook:
    """Represents a phonebook."""

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.contacts: list[Contact] = []
        self.__load_contacts()

    def __load_contacts(self) -> None:
        """Loads contacts from the file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(", ")
                    contact = Contact(*data)
                    self.contacts.append(contact)

    def __save_contacts(self) -> None:
        """Saves contacts to the file."""
        with open(self.file_name, "w", encoding="utf-8") as file:
            for contact in self.contacts:
                file.write(
                    f"{contact.contact_id}, "
                    f"{contact.last_name}, "
                    f"{contact.first_name}, "
                    f"{contact.middle_name}, "
                    f"{contact.organization}, "
                    f"{contact.work_phone}, "
                    f"{contact.personal_phone}\n"
                )

    def __display_contacts(self, page_num: int, page_size: int) -> None:
        """
        Displays a page of contacts.

        Args:
            page_num (int): Page number.
            page_size (int): Number of contacts per page.

        Returns:
            None
        """
        start_idx = (page_num - 1) * page_size
        end_idx = start_idx + page_size

        if len(self.contacts[start_idx:end_idx]) > 0:
            for contact in self.contacts[start_idx:end_idx]:
                print(
                    f"ID: {contact.contact_id} | "
                    f"{contact.last_name} "
                    f"{contact.first_name} "
                    f"{contact.middle_name} | "
                    f"Organization: {contact.organization} | "
                    f"Work phone: {contact.work_phone} | "
                    f"Personal_phone: {contact.personal_phone}"
                )

        elif page_num or page_size < 1:
            print("Page number and page size must be positive integers.")

        else:
            print(f"No contacts found on {page_num} page.")

    def __add_contact(self, contact: Contact) -> None:
        """
        Adds a new contact.

        Args:
            contact (Contact): Contact object to add.

        Returns:
            None
        """
        self.contacts.append(contact)
        self.__save_contacts()
        print("Contact added.")

    def __edit_contact(self, contact_id: int, contact: Contact) -> None:
        """
        Edits an existing contact.

        Args:
            contact_id (int): ID of the contact to edit.
            contact (Contact): Updated contact information.

        Returns:
            None
        """
        self.contacts[contact_id] = contact
        self.__save_contacts()
        print("Contact edited.")

    def __search_contact_by_id(self, contact_id: int) -> None:
        """
        Searches for a contact by ID and displays its information.

        Args:
            contact_id (int): ID of the contact to search.

        Returns:
            None
        """
        try:
            if contact_id < 0:
                raise IndexError
            contact = self.contacts[contact_id]
            print(
                f"ID: {contact.contact_id} | "
                f"{contact.last_name} "
                f"{contact.first_name} "
                f"{contact.middle_name} | "
                f"Organization: {contact.organization} | "
                f"Work phone: {contact.work_phone} | "
                f"Personal_phone: {contact.personal_phone}"
            )

        except IndexError:
            print("Invalid ID. Please try again.")

    def __search_contacts_by_attributes(self, search_values: dict) -> None:
        """
        Searches for contacts based on a query.

        Args:
            search_values (dict): Dictionary with attributes as keys and search queries as values.

        Returns:
            None
        """
        search_results = []
        for contact in self.contacts:
            matching_contact = True
            for attr, value in search_values.items():
                contact_value = getattr(contact, attr).lower()
                if value.lower() not in contact_value:
                    matching_contact = False
                    break
            if matching_contact:
                search_results.append(contact)

        print("Search results:")
        for idx, contact in enumerate(search_results, start=1):
            print(
                f"{idx}. ",
                f"ID: {contact.contact_id} | "
                f"{contact.last_name} "
                f"{contact.first_name} "
                f"{contact.middle_name} | "
                f"Organization: {contact.organization} | "
                f"Work phone: {contact.work_phone} | "
                f"Personal_phone: {contact.personal_phone}",
            )

    def process_display_contacts(self) -> None:
        """
        Processes the display contacts option.

        Returns:
            None
        """
        try:
            page_num = int(input("Enter page number: "))
            page_size = int(input("Enter page size: "))
            self.__display_contacts(page_num, page_size)

        except ValueError:
            print("Invalid input. Page number and page size must be integers")

    def process_add_contact(self) -> None:
        """
        Processes the add contact option.

        Returns:
            None
        """
        try:
            contact_data = ContactPydantic(
                contact_id=len(self.contacts),
                last_name=input("Last Name: "),
                first_name=input("First Name: "),
                middle_name=input("Middle Name: "),
                organization=input("Organization: "),
                work_phone=input("Work Phone: "),
                personal_phone=input("Personal Phone: "),
            )

            new_contact = Contact(
                contact_id=contact_data.contact_id,
                last_name=contact_data.last_name,
                first_name=contact_data.first_name,
                middle_name=contact_data.middle_name,
                organization=contact_data.organization,
                work_phone=contact_data.work_phone,
                personal_phone=contact_data.personal_phone,
            )

        except ValueError as error:
            print(f"Invalid input: {error}")

        else:
            self.__add_contact(new_contact)

    def process_edit_contact(self) -> None:
        """
        Processes the edit contact option.

        Returns:
            None
        """
        try:
            contact_id = int(input("Enter ID of contact to edit: "))
            if contact_id < 0:
                raise IndexError
            edited_contact = copy.copy(self.contacts[contact_id])
            edited_contact.last_name = self.__update_field("Last Name", edited_contact.last_name)
            edited_contact.first_name = self.__update_field("First Name", edited_contact.first_name)
            edited_contact.middle_name = self.__update_field("Middle Name", edited_contact.middle_name)
            edited_contact.organization = self.__update_field("Organization", edited_contact.organization)
            edited_contact.work_phone = self.__update_field("Work Phone", edited_contact.work_phone)
            edited_contact.personal_phone = self.__update_field("Personal Phone", edited_contact.personal_phone)

            contact_data = ContactPydantic(
                contact_id=contact_id,
                last_name=edited_contact.last_name,
                first_name=edited_contact.first_name,
                middle_name=edited_contact.middle_name,
                organization=edited_contact.organization,
                work_phone=edited_contact.work_phone,
                personal_phone=edited_contact.personal_phone,
            )

            edited_contact = Contact(
                contact_id=contact_data.contact_id,
                last_name=contact_data.last_name,
                first_name=contact_data.first_name,
                middle_name=contact_data.middle_name,
                organization=contact_data.organization,
                work_phone=contact_data.work_phone,
                personal_phone=contact_data.personal_phone,
            )

        except IndexError:
            print("Invalid ID. Please try again.")

        except ValueError as error:
            print(f"Invalid input: {error}")

        else:
            self.__edit_contact(contact_id, edited_contact)

    def process_search_contacts(self) -> None:
        """
        Processes the search contacts option.

        Returns:
            None
        """
        print("1. Search by ID.")
        print("2. Search by attributes.")
        choice = input("Select an option: ")

        if choice == "1":
            try:
                contact_id = int(input("Enter a contact ID: "))
                self.__search_contact_by_id(contact_id)
            except ValueError:
                print("Invalid input. ID must be integer. Please try again.")

        elif choice == "2":
            search_values = self.__prepare_search_attributes()
            self.__search_contacts_by_attributes(search_values)

        else:
            print("Invalid option. Please try again.")

    @staticmethod
    def __update_field(field_name: str, current_value: str) -> str:
        """
        Updates a contact field with a new value.

        Args:
            field_name (str): Name of the field to update.
            current_value (str): Current value of the field.

        Returns:
            str: New value for the field if it exists, otherwise the current value.
        """
        new_value = input(f"{field_name} ({current_value}): ").strip()
        return new_value if new_value else current_value

    @staticmethod
    def __prepare_search_attributes() -> dict:
        """
        Prepares search attributes based on user input.

        Returns:
            dict: Dictionary of search attributes and values.
        """
        search_attributes = (
            ("last_name", "Last Name"),
            ("first_name", "First Name"),
            ("middle_name", "Middle Name"),
            ("organization", "Organization"),
            ("work_phone", "Work Phone"),
            ("personal_phone", "Personal Phone"),
        )
        search_values = {}

        for attr, attr_display in search_attributes:
            search_value = input(f"Enter {attr_display} (or leave empty): ").strip()
            if search_value:
                search_values[attr] = search_value

        return search_values
