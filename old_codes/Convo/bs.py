import requests
from bs4 import BeautifulSoup

# Step 1: Get the content of the webpage
url = "https://zissou.infosci.cornell.edu/convokit/datasets/subreddit-corpus/corpus-zipped/"
response = requests.get(url)
webpage_content = response.content

# Step 2: Parse the content with BeautifulSoup
soup = BeautifulSoup(webpage_content, "html.parser")

# Step 3: Extract the file names and sizes
files = []
for link in soup.find_all("a"):
    file_name = link.get("href")
    if file_name.endswith(".zip"):
        file_size = link.next_sibling.strip().split(" ")[-1]
        files.append((file_name, file_size))

# Function to convert file size to bytes for sorting
def convert_size_to_bytes(size):
    size_units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}
    size = size.replace(",", "")
    size_value, size_unit = float(size[:-2]), size[-2:]
    return size_value * size_units[size_unit]

# Step 4: Sort the files by size in descending order
files.sort(key=lambda x: convert_size_to_bytes(x[1]), reverse=True)

# Step 5: Print the sorted files
for file in files:
    print(f"{file[0]}: {file[1]}")
