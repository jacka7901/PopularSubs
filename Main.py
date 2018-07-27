from selenium import webdriver


class Isduplicate:
    dicto = {}

    def read(self):
        f = open(r'C:\Users\jacka\OneDrive\Documents\outputs.txt', "r")

        for line in f:
            k, v = line.strip().split(':')
            self.dicto[k.strip()] = int(v.strip())

        return self.dicto



Is = Isduplicate()



browser = webdriver.Chrome(executable_path=r'C:\Users\jacka\Downloads\chromedriver_win32\chromedriver.exe')

browser.get("https://www.reddit.com/")

elem = browser.find_elements_by_css_selector("a[data-click-id='subreddit']")



'''for line in Is.read():
    k, v = line.split(":")
    dicto[k] = v
'''

counter = 0


text_file = open(r'C:\Users\jacka\OneDrive\Documents\outputs.txt', "a+")

print(len(elem))

while counter < 50:
    e = str(elem[counter].get_attribute("href"))
    e = e.replace("https://www.reddit.com/r/", "")
    e = e[:-1]

    if e in Is.read():
        Is.dicto[e] += 1
    else:
        Is.dicto[e] = 1

    text_file.write(e + ":" + str(Is.dicto[e]) + '\n')

    '''if e in Is.read():
        text_file.write("duplicate found")
    else:
        text_file.write(e + "\n")'''


    print(e)
    counter = counter +2

print(Is.dicto)
text_file.close()
browser.close()



