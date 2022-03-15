from bs4 import BeautifulSoup as bs
import requests

'''------------------------------ Webscraping part ------------------------------'''

#Set up the webscraping stuffs
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

#Initialize the main data list
alldata = []


for index in range(15):
    
    #Get the title
    title = (' '.join(movies[index].get_text().split()[1:-1]))
    
    #Get the link
    link = links[index].attrs.get("href")
    
    #Get the Score 
    score = float(scores[index].get_text())
    
    #Get the review -- Probably there is a better solution    
    review = str(reviews[index])
    start = review.find("on ") + 3
    end = review.find(" user ")
    review = review[start:end]
    review = int(review.replace(",","")) #Remove the "," to get the max value with the max() method
    
    #Get the oscars
    url = f'https://www.imdb.com{link}'
    response = requests.get(url)
    html = response.content
    soup = bs(html, "lxml")
    soup = soup.find('section', class_='ipc-page-section ipc-page-section--base celwidget')
    soup = soup.find('a', class_='ipc-metadata-list-item__label ipc-metadata-list-item__label--link')
    oscar = soup.get_text()[4:-7]
    if len(oscar) != 1:
        oscar = '0'
    oscar = int(oscar)

        
    #Build up the alldata list    
    data = {"Title": title,
           "Link": f'https://www.imdb.com{link}',
           "Score": score,
           "Review": review,
           "Oscar" : oscar}    
    alldata.append(data)


print("The original order: ", alldata)
print("Creating the new order, please wait!")


'''------------------------------ Data manipulating part ------------------------------'''

#Get the maximum review
reviewslist = []
for data in alldata: 
    reviewslist.append(data['Review']) 
maxreview = max(reviewslist)


for data in alldata:

    #Change the score value depending on the review
    if data['Review'] < maxreview:
        data['Score'] = (data['Score'] - ((maxreview - data['Review']) / 100000) * 0.1)

    #Change the score value depending on the number of oscars
    if data['Oscar'] != 0:
        data['Score'] = data['Score'] + (data['Oscar'] * 0.5)

#Ascendig order by Score value
alldata = sorted(alldata, key = lambda i: i['Score'], reverse = True)

print("The new order: ", alldata)