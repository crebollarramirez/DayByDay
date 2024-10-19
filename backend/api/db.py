import argparse
from .Dynamo import DynamoDB_Manager

# Initialize the parser
parser = argparse.ArgumentParser(description="Manipulating the table")

# Define the arguments
parser.add_argument("-d", action="store_true", help="Deletes Table")
parser.add_argument("-n", action="store_true", help="Creates Table")
parser.add_argument("-a", action="store_true", help="Add dummy values")
parser.add_argument("-s", action="store_true", help="Show Table")
parser.add_argument("-c", action="store_true", help="Clear Table")
parser.add_argument(
    "-A", action="store_true", help="Reset Table, add dummy data, and display table"
)

# Parse the arguments
args = parser.parse_args()

# Debugging output to check if args are parsed
print(args)

# Conditional checks for the flags
if args.d:
    DynamoDB_Manager.delete_table()

if args.n:
    DynamoDB_Manager.create_dynamodb_table()

if args.a:
    DynamoDB_Manager.addDummyData()

if args.s:
    DynamoDB_Manager.show()

if args.c:
    DynamoDB_Manager.clear_table()

if args.A:
    DynamoDB_Manager.clear_table()
    # DynamoDB_Manager.addDummyData()
    DynamoDB_Manager.show()