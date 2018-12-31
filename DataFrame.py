from selenium import webdriver
from flask import Flask, render_template
import pandas as pd
import numpy as np
elem = ""

#loop prevents crashing due to the old version of reddit loading
while not elem:
    browser = webdriver.Chrome(executable_path=r'C:\Users\jacka\Downloads\chromedriver_win32\chromedriver.exe')
    browser.get("https://www.reddit.com/")
    elem = browser.find_elements_by_css_selector("a[data-click-id='subreddit']")

Location = r'C:\Users\jacka\OneDrive\Documents\outputs.csv'
df = pd.read_csv(Location, index_col=False)

counter = 0
while counter < 50:
    e = str(elem[counter].get_attribute("href"))
    e = e.replace("https://www.reddit.com/r/", "")
    e = e[:-1]

    if e in df['Subreddit'].values:
        df.loc[df['Subreddit'] == e, 'Appearances'] += 1
    else:
        df = df.append({'Subreddit': e, 'Appearances': 1}, ignore_index=True)

    print(e)
    # because there are 2 html tags of the same subreddit name, we have to increment by 2 each time.
    counter = counter + 2


df.sort_values(by='Appearances', ascending=False,  inplace=True)
# resets the indexes to display rankings correctly.
df.reset_index(drop=True, inplace=True)
df.to_csv(Location, index=False)
# after writing the data to the csv, the index is set to start at 1 instead of 0, for design purposes.
df.index = np.arange( 1, len(df) + 1)

df1 = df.loc[:33, :]
df2 = df.loc[34:66, :]
df3 = df.loc[67:99, :]

print(df)
print(df1)
print(df2)
print(df3)

browser.close()

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("Pop.html", dataframe1 = df1, dataframe2 = df2, dataframe3 = df3, )
if __name__ == "__main__":
    app.run(debug=False)




#top 50, then hit "more"