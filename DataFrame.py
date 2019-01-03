from selenium import webdriver
from flask import Flask, render_template
import pandas as pd
import numpy as np
import time
import threading
import boto3
import s3fs
import os
from selenium.webdriver.chrome.options import Options


def updatetable():
    while True:
        elem = ""

        #loop prevents crashing due to the old version of reddit loading
        while not elem:
            chrome_options = Options()
            chrome_options.binary_location = os.environ['GOOGLE_CHROME_BIN']
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--headless')

            browser = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], chrome_options=chrome_options)
            #browser = webdriver.Chrome(executable_path=r'C:\Users\jacka\Downloads\chromedriver_win32\chromedriver.exe')
            browser.get("https://www.reddit.com/")
            elem = browser.find_elements_by_css_selector("a[data-click-id='subreddit']")


        objectkey = 'outputs.csv'
        bucketname = 'popularsubs'
        #reading and converting the .csv file in the s3 bucket to a dataframe
        s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        read_file = s3.get_object(Bucket=bucketname, Key=objectkey)
        df = pd.read_csv(read_file['Body'], index_col= False)

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
        #writing to the .csv file in the s3 bucket
        bytes_to_write = df.to_csv(None, index=False).encode()
        fs = s3fs.S3FileSystem(key=os.environ['AWS_ACCESS_KEY_ID'], secret=os.environ['AWS_SECRET_ACCESS_KEY'])
        with fs.open('s3://popularsubs/outputs.csv', 'wb') as f:
            f.write(bytes_to_write)

        # after writing the data to the csv, the index is set to start at 1 instead of 0, for design purposes.
        df.index = np.arange( 1, len(df) + 1)

        global df1, df2, df3
        df1 = df.loc[:33, :]
        df2 = df.loc[34:66, :]
        df3 = df.loc[67:99, :]

        print(df)
        print(df1)
        print(df2)
        print(df3)

        browser.close()
        time.sleep(10)


app = Flask(__name__)
@app.route('/')
def index():
    return render_template("Pop.html", dataframe1 = df1, dataframe2 = df2, dataframe3 = df3, )

threading.Thread(target=updatetable).start()

if __name__ == "__main__":
    app.run(debug=False)





