from bs4 import BeautifulSoup as bs
import requests


url = "https://www.imdb.com/chart/top/"
response = requests.get(url)
html = response.content
soup = bs(html, "lxml")

print("The process will take a few minutes")

#Get every movies links scores reviews
movies = soup.select('td.titleColumn')
links = soup.select('td.titleColumn a')
scores = soup.select('td.ratingColumn strong')
reviews = soup.select('td.ratingColumn strong')

alldata = []


for index in range(10):
    
    #Get the title
    title = (' '.join(movies[index].get_text().split()[1:-1]))
    
    #Get the link
    link = links[index].attrs.get("href")
    
    #Get the review
    score = scores[index].get_text()
        
    review = str(reviews[index])
    start = review.find("on ") + 3
    end = review.find(" user ")
    review = review[start:end]
    
    #Get the oscars
    url = f"https://www.imdb.com{link}"
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")
    soup = soup.find('section', class_='ipc-page-section ipc-page-section--base celwidget')
    soup = soup.find('a', class_='ipc-metadata-list-item__label ipc-metadata-list-item__label--link')
    oscar = soup.get_text()[4:-7]
    if len(oscar) != 1:
        oscar = '0'

        
        
    data = {"Title": title,
           "Link": f'https://www.imdb.com{link}',
           "Score": score,
           "Review": review,
           "Oscar" : oscar}
    
    alldata.append(data)

print(alldata)

