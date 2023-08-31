import requests
from bs4 import BeautifulSoup
import csv

for page_number in range(0, 80):  # Assuming you want to scrape 20 pages
    start_value = page_number * 50 + 1  # Calculate the 'start' value for each page
    url = f"https://www.imdb.com/search/title/?title_type=feature&primary_language=ml&sort=year,desc&start={start_value}"


    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        lister_items = soup.find_all(class_="lister-item mode-advanced")

        for item in lister_items:
            content = item.find(class_="lister-item-content")

            # Extracting title
            title_element = content.find("h3", class_="lister-item-header").find("a")
            title = title_element.get_text() if title_element else "null"

            # Extracting genre
            genre_element = content.find("span", class_="genre")
            genre = genre_element.get_text(strip=True) if genre_element else "null"

            # Extracting description
            description_element = content.find("p", class_="text-muted").find_next_sibling("p", class_="text-muted")
            description = description_element.get_text(strip=True) if description_element else "null"

            # Extracting director's name
            director_element = content.find("p", class_="").find("a")
            director_name = director_element.get_text() if director_element else "null"

            # Extracting stars' names
            stars_elements = content.find_all("a", href=True, class_="")
            stars_names = [star.get_text() for star in stars_elements if "/name/nm" in star["href"] and star.get_text() != director_name]

            print("Title:", title)
            print("Genre:", genre)
            print("Description:", description)
            print("Director:", director_name)
            print("Stars:", ", ".join(stars_names))  # Join the stars' names into a comma-separated string

            # Append the details to a CSV file
            with open("full_details.csv", "a", newline="", encoding="utf-8") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([title, genre, description, director_name,stars_names])

        print(f"Details appended to 'full_details.csv' file of {page_number}.")
    else:
        print("Failed to retrieve the webpage.")
