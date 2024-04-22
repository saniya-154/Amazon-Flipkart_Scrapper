import json

def remove_null_values(data):
    return [entry for entry in data if all(entry.values())]

def remove_duplicates(data, key=lambda x: x):
    seen = set()
    unique_data = []
    for entry in data:
        entry_key = key(entry)
        if entry_key not in seen:
            seen.add(entry_key)
            unique_data.append(entry)
    return unique_data

def main():
    # Load JSON data from file
    with open('C:\\Users\\dell\\My Scrapy Prj\\scrapper\\products.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Remove null values
    data_without_null = remove_null_values(data)

    # Remove duplicates based on the 'name' field
    cleaned_data = remove_duplicates(data_without_null, key=lambda x: x['name'])

    # Write cleaned data to a new JSON file
    with open('C:\\Users\\dell\\My Scrapy Prj\\scrapper\\cleaned_products.json', 'w') as file:
        json.dump(cleaned_data, file, indent=4)

if __name__ == "__main__":
    main()
