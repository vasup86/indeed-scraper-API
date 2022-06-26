import requests
from bs4 import BeautifulSoup as BS

class Backend:

    def __init__(self, title, location, pages,country, distance, date):
        self.title = title
        self.location = location
        self.pages = int(pages)
        self.country = country
        self.distance = distance
        self.date = date
        self.joblist = []

    def scrape(self):
        url = f'https://{self.country}.indeed.com/jobs?q='
        combUrl = url + (self.title.replace(" ", "+")) + "&l=" + (self.location.replace(", ", "%2C%20"))

        if(self.distance== "Distance in KM" and self.date == 'D'):   #neither is selected
            for i in range(0, (self.pages*10), 10): #(0 to 30 in step of 10)
                c = self.extract(i, combUrl) # i is the page # of the url search
                self.transform(c)
                
        elif(self.distance!="Distance in KM" and self.date=='D'):   #only distance is selected
            #distance: &radius=(#of km), exact=0
            combUrl = combUrl + "&radius="+ str(self.distance)
            for i in range(0, (self.pages*10), 10): #(0 to 30 in step of 10)
                c = self.extract(i,combUrl) # i is the page # of the url search
                self.transform(c)

        elif(self.distance=="Distance in KM" and self.date!='D'): #only time is selected
            #time: &fromage=(time), 24 hr = 1
            combUrl = combUrl + "&fromage=" + str(self.date)
            for i in range(0, (self.pages*10), 10): #(0 to 30 in step of 10)
                c = self.extract(i,combUrl) # i is the page # of the url search
                self.transform(c)

        else:    #if both are selected
            combUrl = combUrl + "&radius="+ str(self.distance) + "&fromage=" + str(self.date)
            for i in range(0, (self.pages*10), 10): #(0 to 30 in step of 10)
                c = self.extract(i,combUrl) # i is the page # of the url search
                self.transform(c)

        return self.joblist

    
    def extract(self, page, combUrl):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        #{}, .format is for the the page# 
        combUrl = (combUrl+ "&start={}").format(page)
        print(combUrl)
        r = requests.get(combUrl, headers)
        soup = BS(r.content, "html.parser")
        return soup

    def transform(self, soup):
        ul = soup.find('ul', class_='jobsearch-ResultsList')
        li = ul.find_all('li')  #basic class name for each job post shell
        #print(len(li))
        i = 1
        for item in li:
            if item is None:
                continue
            try:
                #title = item.find('a').text.strip()  #class title, is an 'a' tag, and has title as text
                partTitle = item.find('h2', class_="jobTitle") #.text.strip("new")  #class jobTitle, is an 'h2' tag, and has title as text
                title = partTitle.find('a').text
                #print(title)

                company = item.find("span", class_="companyName").text.strip()
                # print(company)

                location = item.find("div", class_="companyLocation").text.strip()

                try:
                    jobType = item.find_all("div", class_="attribute_snippet")
                    if(len(jobType) == 1):
                        jobType = jobType[0].text.strip()
                        # print(jobType)
                    else:
                        jobType = jobType[1].text.strip()
                        # print(jobType)
                except:
                    jobType = ""

                try:
                    salary = item.find("div", class_="salary-snippet-container").text.strip()
                except:
                    salary = ""
                
                # try:
                #     jobType = item.find("div", class_="attribute_snippet").text.strip()
                # except:
                #     jobType = ""
                
                try:
                    href = item.find('a').attrs["data-jk"]
                    link = (f'https://{self.country}.indeed.com/viewjob?jk={href}')
                except:
                    link = ""
                
                try:
                    summary = item.find("div", class_="job-snippet").text.strip()
                except:
                    summary = ""
                
                try:
                    date = item.find("span", class_="date").text.strip("Posted")
                    date = date.replace("Hiring ongoing", "")
                    date = date.replace("ag", "ago")
                    date = date.replace("EmployerActive ", "")
                    #print(date)
                except:
                    date = ""

                job = {
                    'key':i,
                    'title': title,
                    'company': company,
                    'location':location,
                    'type':jobType,
                    'salary': salary,
                    'jobLink': link,  #use i as a ref for which itteration of for loop is on, and insert the link accordingly
                    'summary': summary,
                    "date":date
                }
                #print(job)
                i+=1
                self.joblist.append(job)

            except:
                pass