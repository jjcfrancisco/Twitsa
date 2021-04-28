from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud

import time
from datetime import datetime, date
from time import sleep
import re

import tkinter as tk

#Main function that calls the application
def main(word, lang, lat, lon, km):
    #Set path of search engine & initiate the driver

    #Sets path for search engine, initiates the driver, caches the Twitter page
    PATH = "/Applications/chromedriver"
    driver = webdriver.Chrome(PATH)
    driver.get("https://twitter.com/explore")
    wait = WebDriverWait(driver,10)
    sleep(10)

    #Searches for Twitter search bar using xpath
    search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')

    #User inputs
    search_input.send_keys(word + ' ' + lang + ' ' + 'geocode:' + str(lat) + ',' + str(lon) + ',' + str(km) + 'km')

    search_input.send_keys(Keys.RETURN)
    sleep(10)

    #Clicks on the tab 'latest'
    driver.find_element_by_link_text('Latest').click()

    #Collects all tweets in page
    data = []
    tweet_ids = set()
    last_position = driver.execute_script("return window.pageYOffset;")
    scrolling = True

    def get_tweet_data(card):
        #Extracts tweet from the element
        username = card.find_element_by_xpath('.//span').text
        
        
        try:
            handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
        except NoSuchElementException:
            return
        
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
        
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        text = comment + ' ' + responding
        reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
        retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
        like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text
        
        # get a string of all emojis contained in the tweet
        """Emojis are stored as images... so I convert the filename, which is stored as unicode, into 
        the emoji character."""
        emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
        emoji_list = []
        for tag in emoji_tags:
            filename = tag.get_attribute('src')
            try:
                emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
            except AttributeError:
                continue
            if emoji:
                emoji_list.append(emoji)
        emojis = ' '.join(emoji_list)
        
        tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt)
        return tweet

    while scrolling:
        page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        for card in page_cards[-15:]:
            tweet = get_tweet_data(card)
            if tweet:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
            
        scroll_attempt = 0
        while True:
            # check scroll position
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(2)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1
                
                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    sleep(2) # attempt another scroll
            else:
                last_position = curr_position
                break
    
    # close the web driver
    driver.close()

    def cleanTweets1():
        tweetList = []
        for i in data:
            tweetList.append(i)
        df = pd.DataFrame(tweetList)
        df = df.rename(columns={df.columns[0]: 'username', df.columns[1]: 'handle', df.columns[2]: 'date', df.columns[3]: 'message', df.columns[4]: 'emojis', df.columns[5]: 'reply_cnt', df.columns[6]: 'retweet_cnt', df.columns[7]: 'like_cnt'})
        return df

    df = cleanTweets1()

    def cleanTweets2(text):
        text = re.sub(r'#', ' ', text)
        text = re.sub(r'\n', ' ', text)
        text = re.sub('(?:\s)@[^, ]*', '', text)

        text = re.sub(r'@[A-Za-z0-9]+', '', text)
        text = re.sub(r'Replying to[\s]+', '', text)
        return text
    
    df['message'] = df['message'].apply(cleanTweets2)

    #Get subjectivity & polarity using TextBlob library
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    #Subjectivity and polarity functions implemented
    df['subjectivity'] = df['message'].apply(getSubjectivity)
    df['polarity'] = df['message'].apply(getPolarity)

    #Get results and store them in the df column as 'positive', 'neutral', 'negative'
    def getAnalysis(score):
        if score < 0:
            return 'negative'
        elif score == 0:
            return 'neutral'
        else:
            return 'positive'

    df['analysis'] = df['polarity'].apply(getAnalysis)

    #Get results and store them in the df column as 'positive', 'neutral', 'negative'
    def getAnalysis(score):
        if score < 0:
            return 'negative'
        elif score == 0:
            return 'neutral'
        else:
            return 'positive'

    df['analysis'] = df['polarity'].apply(getAnalysis)

    df['word'] = word

    def getWordCloud():
        #A visual representation #1: strength of words scrapped using WordCloud library
        everyWord = ' '.join([tweets for tweets in df['message']])
        wordCloud = WordCloud(width= 500, height = 300, random_state = 21, max_font_size = 110).generate(everyWord)

        sentWordCloud = plt.figure(figsize=(8,6))
        plt.imshow(wordCloud, interpolation = 'bilinear')
        plt.axis('off')
        sentWordCloud.savefig('sentiment-wordcloud.pdf')

    getWordCloud()

    def getSentPolFig():
        #A visual representation #2: observe subjectivity and polarity in a scatter plot
        sentPolFig = plt.figure(figsize=(8,6))
        for i in range(0, df.shape[0]):
            plt.scatter(df['polarity'][i], df['subjectivity'][i], color='Blue')

        plt.title('Sentiment Analysis')
        plt.xlabel('Polarity')
        plt.ylabel('Subjectivity')
        sentPolFig.savefig('sentiment-polarity.pdf')

    getSentPolFig()

    def getSentPercFig():
        #A visual representation #3: bar plot of positive, negative and neutral tweets
        sentPerc = plt.figure(figsize=(8,6))

        plt.title('Sentiment Analysis')
        plt.xlabel('Sentiment')
        plt.ylabel('Counts')
        df.analysis.value_counts().plot(kind='bar')
        sentPerc.savefig('sentiment-percentage.pdf')

    getSentPercFig()

    def getCsv():
        #Exports the df to CSV
        now = datetime.now()
        timeNow = now.strftime("%d-%m-%Y %H:%M:%S")
        df.to_csv('twitter-sentiment-analysis' + ' - ' + timeNow + '.csv')

    getCsv()

    #Making descriptive stats of positive, negative and neutral tweets
    postweets = df[df.analysis == 'positive']
    postweets = postweets['message']

    neutweets = df[df.analysis == 'neutral']
    neutweets = neutweets['message']

    negtweets = df[df.analysis == 'negative']
    negtweets = negtweets['message']

    postwtperc = str(round((postweets.shape[0] / df.shape[0]) *100, 1)) + "% of people made positive comments about " + word
    neutwtperc = str(round((neutweets.shape[0] / df.shape[0]) *100, 1)) + "% of people made neutral comments about " + word
    negtwtperc = str(round((negtweets.shape[0] / df.shape[0]) *100, 1)) + "% of people made negative comments about " + word

    #Amount of tweets collected
    numberOfTweets = "Tweets extracted: " + str(len(df))

    return [numberOfTweets, postwtperc, neutwtperc, negtwtperc]

####################

def clickGo():
    global wordEntry, latEntry, lonEntry, kmEntry
    processing = tk.Label(root, text="Processing...")
    processing.grid(row=8, columns=1, columnspan=2, pady=(0, 20))
    root.update()

    results = main(wordEntry.get(), "lang:en", float(latEntry.get()), float(lonEntry.get()), float(kmEntry.get()))

    processing.destroy()

    resultsBanner = tk.Label(root, text="#### The Results: ####")
    resultsBanner.grid(row=9, columns=1, columnspan=2, pady=20)

    results1 = tk.Label(root, text=results[0])
    results1.grid(row=10, columns=1, columnspan=2, padx=25)

    results2 = tk.Label(root, text=results[1])
    results2.grid(row=11, columns=1, columnspan=2, padx=25)

    results3 = tk.Label(root, text=results[2])
    results3.grid(row=12, columns=1, columnspan=2, padx=25)

    results4 = tk.Label(root, text=results[3])
    results4.grid(row=13, columns=1, columnspan=2, padx=25, pady=(0, 20))

    note = tk.Label(root, text="**Additional two graphs and a CSV file have been created in the root folder.")
    note.grid(row=14, columns=1, columnspan=2, padx=25, pady=(0, 20))    

    resultsBanner.config(font=("Georgia", 20, "bold"))
    results1.config(font=("Georgia", 15))
    results2.config(font=("Georgia", 15))
    results3.config(font=("Georgia", 15))
    results4.config(font=("Georgia", 15))
    note.config(font=("Georgia", 15, "italic"))



root = tk.Tk()
root.title("Twitsa")
#root.geometry("800x600")

logoLabel = tk.Label(root, text="Twitsa")
introLabel = tk.Label(root, text="Twitsa app searches a given word on Twitter and \n gives an in depth sentiment analysis.")
optionsLabel = tk.Label(root, text="Please note:\n Only enter one word and only \n use coordinates in decimal degrees.")

wordLabel = tk.Label(root, text="Word:")
wordEntry = tk.Entry(root)
latLabel = tk.Label(root, text="Latitude:")
latEntry = tk.Entry(root)
lonLabel = tk.Label(root, text="Longitude:")
lonEntry = tk.Entry(root)
kmLabel = tk.Label(root, text="Distance in Km:")
kmEntry = tk.Entry(root)

logoLabel.grid(row=0, column=0, pady=5, columnspan=2)
introLabel.grid(row=1, column=0, columnspan=2, pady=(0, 20))
optionsLabel.grid(row=2, column=0, columnspan=2, pady=(0, 20))

wordLabel.grid(row=3, column=0)
wordEntry.grid(row=3, column=1)
wordEntry.focus_set()
latLabel.grid(row=4, column=0)
latEntry.grid(row=4, column=1)
lonLabel.grid(row=5, column=0)
lonEntry.grid(row=5, column=1)
kmLabel.grid(row=6, column=0)
kmEntry.grid(row=6, column=1)

button = tk.Button(root, text="Go", command=clickGo)
button.grid(row=7, column=0, columnspan=2, pady=20)

cr = tk.Label(root, text="App created by Frank Jimenez | " + str(datetime.now().year))
cr.grid(row=15, column=0, columnspan=2, pady=20)

logoLabel.config(font=("Georgia", 44))
introLabel.config(font=("Georgia", 15))
optionsLabel.config(font=("Georgia", 15))
wordLabel.config(font=("Georgia", 13, "bold"))
latLabel.config(font=("Georgia", 13, "bold"))
lonLabel.config(font=("Georgia", 13, "bold"))
kmLabel.config(font=("Georgia", 13, "bold"))
button.config(font=("Georgia", 20, "bold"))
cr.config(font=("Georgia", 11, "bold"))

root.mainloop()