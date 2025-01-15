from bs4 import BeautifulSoup

with open("./mock_files/test.html", "r") as file:
    data = file.read()

soup = BeautifulSoup(data, "html.parser")

#print(soup.prettify())

book_entries = soup.find_all("div", class_="book-entry")

for b in book_entries:
    title = b.find('h2').text
    author = b.find(class_="author").text
    print(title)
    print(author)

sales_table = soup.find("table", class_="sales-table")
tbody = sales_table.find("tbody")
rows = tbody.find_all("tr")

for r in rows:
    cat = r['data-category']
    print(cat)