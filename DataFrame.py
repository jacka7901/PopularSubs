from selenium import webdriver
import pandas as pd


class DataFrame:
    browser = webdriver.Chrome(executable_path=r'C:\Users\jacka\Downloads\chromedriver_win32\chromedriver.exe')

    browser.get("https://www.reddit.com/")

    # grabs the html tag for the subreddit name
    elem = browser.find_elements_by_css_selector("a[data-click-id='subreddit']")

    # output locations
    Location = r'C:\Users\jacka\OneDrive\Documents\outputs.csv'
    # set dataframe to csv file
    df = pd.read_csv(Location)

    print(len(elem))


    def updateDataFrame(self):
        counter = 0
        while counter < 50:

            # gets just the subreddit name
            e = str(self.elem[counter].get_attribute("href"))
            e = e.replace("https://www.reddit.com/r/", "")
            e = e[:-1]

            if e in self.df['Subreddit'].values:
                # adds 1 to Appearances if the subreddit is already in the DF
                self.df.loc[self.df['Subreddit'] == e, 'Appearances'] += 1
            else:
                # adds new row with the subreddit name and sets the amount of appearances to 1.
                self.df = self.df.append({'Subreddit': e, 'Appearances': 1}, ignore_index=True)

            print(e)
            #because there are 2 html tags of the same subreddit name, we have to increment by 2 each time.
            counter = counter + 2

    def save(self):
        # saves DataFrame to csv file
        self.df.to_csv(self.Location, index=False)


class Main:
    dataframe = DataFrame()

    dataframe.updateDataFrame()
    print(dataframe.df)
    dataframe.save()

    dataframe.browser.close()
