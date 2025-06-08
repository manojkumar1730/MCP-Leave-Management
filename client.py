import sys
from main import employee_leaves  # Import data to get name and age

def show_menu():
    print("\nWelcome to the MCP Leave Manager Client")
    print("1. Check Leave Balance")
    print("2. Apply for Leave")
    print("3. View Leave History")
    print("4. Get Greeting")
    print("5. Exit")

def start_client():
    from main import get_leave_balance, apply_leave, get_leave_history, get_greeting

    employee_id = input("Enter your Employee ID (e.g., E001): ").strip()

    # Display name and age
    if employee_id in employee_leaves:
        emp_data = employee_leaves[employee_id]
        print(f"\nWelcome {emp_data['name']} (Age: {emp_data['age']})")
    else:
        print("Employee ID not found.")
        return

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            print(get_leave_balance(employee_id))

        elif choice == "2":
            dates = input("Enter leave dates separated by commas (e.g., 2025-07-10,2025-07-11): ")
            leave_dates = [d.strip() for d in dates.split(",") if d.strip()]
            print(apply_leave(employee_id, leave_dates))

        elif choice == "3":
            print(get_leave_history(employee_id))

        elif choice == "4":
            name = input("Enter your name: ")
            print(get_greeting(name))

        elif choice == "5":
            print("Exiting client. Goodbye!")
            break

        else:
            print("Invalid choice. Please select from the menu.")

if __name__ == "__main__":
    start_client()
