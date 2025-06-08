from mcp.server.fastmcp import FastMCP
from typing import List
import csv

# Load employee leave data from CSV
def load_data_from_csv(filepath: str) -> dict:
    data = {}
    with open(filepath, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            history_list = row['history'].split(';') if row['history'] else []
            data[row['employee_id']] = {
                "name": row['name'],
                "age": int(row['age']),
                "balance": int(row['balance']),
                "history": history_list
            }
    return data

# Save updated leave data back to CSV
def save_data_to_csv(filepath: str, data: dict):
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["employee_id", "name", "age", "balance", "history"])
        for emp_id, details in data.items():
            history = ';'.join(details["history"])
            writer.writerow([emp_id, details.get("name", ""), details.get("age", ""), details["balance"], history])

# Load data from CSV
employee_leaves = load_data_from_csv("leave_data.csv")

# Create MCP server
mcp = FastMCP("LeaveManager")

# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Check how many leave days are left for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return "Employee ID not found."

# Tool: Apply for Leave with specific dates
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    if employee_id not in employee_leaves:
        return "Employee ID not found."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

    # Deduct balance and add to history
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)

    # Save updated data to CSV
    save_data_to_csv("leave_data.csv", employee_leaves)

    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."

# Resource: Leave history
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_id}: {history}"
    return "Employee ID not found."

# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"

if __name__ == "__main__":
    mcp.run()
