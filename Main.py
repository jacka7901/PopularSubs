from selenium import webdriver
import pandas as pd


class Isduplicate:
    dicto = {}




    browser = webdriver.Chrome(executable_path=r'C:\Users\jacka\Downloads\chromedriver_win32\chromedriver.exe')

    browser.get("https://www.reddit.com/")

    #grabs the html tag for the subreddit name
    elem = browser.find_elements_by_css_selector("a[data-click-id='subreddit']")

    counter = 0

    #output locations
    text_file = open(r'C:\Users\jacka\OneDrive\Documents\outputs.csv', "a+")
    Location = r'C:\Users\jacka\OneDrive\Documents\outputs.csv'

    df = pd.read_csv(Location)
    print(df)

    print(len(elem))

    while counter < 50:

        #gets just the subreddit name
        e = str(elem[counter].get_attribute("href"))
        e = e.replace("https://www.reddit.com/r/", "")
        e = e[:-1]

        df = df.append({'Subreddit' : e}, ignore_index=True)

        if e in df:
            dicto[e] += 1
        else:
            dicto[e] = 1

        #text_file.write(e + "," + str(dicto[e]) + '\n')



        print(e)
        counter = counter + 2

    print(df)
    text_file.close()
    browser.close()
