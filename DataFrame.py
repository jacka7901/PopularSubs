from selenium import webdriver
import pandas as pd

elem = ""
#loop prevents crashing due to the old version of reddit loading
while not elem:
    browser = webdriver.Chrome(executable_path=r'C:\Users\jacka\Downloads\chromedriver_win32\chromedriver.exe')
    browser.get("https://www.reddit.com/")
    elem = browser.find_elements_by_css_selector("a[data-click-id='subreddit']")


Location = r'C:\Users\jacka\OneDrive\Documents\outputs.csv'
df = pd.read_csv(Location)
print(len(elem))

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

print(df)
df.to_csv(Location, index=False)

browser.close()
