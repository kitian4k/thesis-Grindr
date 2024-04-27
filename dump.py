import sys

def main(data):
    print("Received data:")
    print(data)
    print(type(data))

if __name__ == "__main__":
    # Check if data argument is provided
    if len(sys.argv) > 1:
        data = sys.argv[1]
        main(data)
    else:
        print("No data provided.")
