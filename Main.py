from selenium import webdriver
import pandas as pd


class Isduplicate:
    L = []




    browser = webdriver.Chrome(executable_path=r'C:\Users\jacka\Downloads\chromedriver_win32\chromedriver.exe')

    browser.get("https://www.reddit.com/")

    #grabs the html tag for the subreddit name
    elem = browser.find_elements_by_css_selector("a[data-click-id='subreddit']")

    counter = 0

    #output locations
    text_file = open(r'C:\Users\jacka\OneDrive\Documents\outputs.csv', "a+")
    Location = r'C:\Users\jacka\OneDrive\Documents\outputs.csv'

    df = pd.read_csv(Location)


    print(len(elem))

    while counter < 50:

        #gets just the subreddit name
        e = str(elem[counter].get_attribute("href"))
        e = e.replace("https://www.reddit.com/r/", "")
        e = e[:-1]



        if e in df['Subreddit'].values:
            #adds 1 to Appearances if the subreddit is already in the DF
            df.loc[df['Subreddit'] == e, 'Appearances'] += 1
        else:
            #adds new row with the subreddit name and sets the amount of appearances to 1.
            df = df.append({'Subreddit': e, 'Appearances': 1}, ignore_index=True)

        df.reset_index(inplace=True, drop=True)

        print(e)
        counter = counter + 2

    #df.drop(df.columns[df.columns.str.contains('Unnamed', case=False)], axis=1)

    print(df)


    #saves DataFrame to csv file
    df.to_csv(r'C:\Users\jacka\OneDrive\Documents\outputs.csv')

    text_file.close()
    browser.close()
