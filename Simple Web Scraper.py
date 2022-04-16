import urllib
import requests
from bs4 import BeautifulSoup
#Import needed resources

class Movie:
    # constructor
    def __init__(self, move_name, move_ranking, move_year, move_rating, move_type):
        self.move_name = move_name
        self.move_ranking = move_ranking
        self.move_year = move_year
        self.move_rating = move_rating
        self.move_type = move_type

    # Writing information with specific style
    def WriteInformation(self):
        return "Movie Name: " + str(self.move_name) + "\n" \
               + "Movie Ranking: " + str(self.move_ranking) + "\n" \
               + "Movie Release Year: " + str(self.move_year) + "\n" \
               + "Movie Stars(1-10): " + str(self.move_rating) + "\n" \
               + "Movie Type: " + str(self.move_type) + "\n" + "*" * 50 + "\n"

# Scrape function to get values from website
def scrap():
    try:
        text = urllib.request.urlopen("https://www.imdb.com/list/ls051781075/")
        tag = BeautifulSoup(text, 'html.parser')

        # items mean each movie with several attributes going to be extracted
        items = tag.find_all('div', class_="lister-item-content")

        # movie_info to store extracted data
        movie_info = []

        for eachMovie in items:
            # scrape 5 stipulated data from each movie item
            move_name = eachMovie.find('a').string
            move_ranking = eachMovie.find('span', class_='lister-item-index unbold text-primary').string
            move_year = eachMovie.find('span', class_='lister-item-year text-muted unbold').string
            move_rating = eachMovie.find('span', class_='ipl-rating-star__rating').string
            move_type = eachMovie.find('span', class_='genre').string.strip()

            # Add 5 attributes to Movie class and append it in movie_info list
            movie_info.append(Movie(move_name,move_ranking,move_year,move_rating,move_type))
        return movie_info

    except:
        print("Your retrieval request was unsuccessful.")

def BuildDic():
    try:
        # create list to store dictionaries, dic stores 5 attributes for each movie item which is easy for search
        list = []
        dic = {}

        # Read information from generated file
        f = open("movie_info.txt", "r")
        while f:
            line = f.readline()
            # Every time read star line, append current dic which is one movie_item to list
            if line.__contains__('*'):
                list.append(dic.copy())

            # Build dictionary for each movie item
            elif line != "":
                key = line.split(": ")[0]
                value = line.split(": ")[1].strip()
                dic[key] = value
            else:
                break

        f.close()

        return list
    except:
        print("File movie_info.txt does not exsit.")

def main():
    print("Retrieving Top 100 Movies from the IMBD database and saving it in movie_info.txt file...")

    # scrap and pass values to movie_info
    movie_info = scrap()
    with open("movie_info.txt", "w") as f:
        for movie in movie_info:
            # Calling get_string method to create strings out of each gene's attributes and write it into file.
            each_movie = movie.WriteInformation()
            f.write(each_movie)

    print("Retrieval complete. Goodbye, Result is below:.")

    # show scraped information from movie_info file, and print it out in dictionary style
    for i in BuildDic():
        print(i)

if __name__ == '__main__':
    main()