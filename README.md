# Indeed Scraper Website

website: https://indeed-scraper-react.netlify.app/
 
Website (frontend) is hosted on netlify and backend is hosted on heroku.

Scraping API (backend): https://indeed-scraper-react.herokuapp.com/api/scrape

## About
The API was developed using flask, requests and BeautifulSoup. Currently, only 1 API is supported (above link). The API takes a JSON object with information descibed under documentation and returns an array of JSON objects (dict) of job listings. The website works for all current Indeed worldwide domains ([List](https://www.indeed.com/worldwide)). 

## Documentation
link: https://indeed-scraper-react.herokuapp.com/api/scrape

### POST
The API takes a JSON object with following paramater **title**  <sup>[1]</sup>, **location**  <sup>[2]</sup>, **pages**  <sup>[3]</sup>, **country**  <sup>[4]</sup>, **distance**  <sup>[5]</sup>, **date**  <sup>[6]</sup>. (all parameters are mandatory)
\
headers: {'Content-Type':"application/json"}<br>
[1] title (string): Job posting title ex: software developer, baker, cashier, ... <br>
[2] location (string): city of job listing, ex: Toronto, new york, miami<br>
[3] pages (int): No of pages worth of job listings user wants to scrape. 1 page contains 15 job positings.<br>
[4] country: ISO country code (for united states, use 'www' instead of 'us').  Ex: Canada: ca.<br>
[5] distance:  Job search radius based on input location.
	
 - Default (no distance): 'Distance in KM'
 - Exact: 'exact'
 - 5 KM : '5'
 - 10 KM : '10'
 - 15 KM : '15'
 - 20 KM : '20'
 - 50 KM : '50'
 - 100 KM : '100'

[6] date: When the job listing was posted, ex: 3 days will show only job listings posted in last 3 days.<br>
 - Default (no preference): 'D'
 -  24 hrs : '24'
 - 3 days: '3'
 - 7 days: '7'
 - 14 days: '14'
 
Ex:
```
{
	"title":  "software developer",
	"location":  "Toronto",
	"pages":  2,
	"country":  "ca",
	"distance": "Distance in KM",
	"date" : "14",
}
```
Ex:
```
{
	"title":  "baker",
	"location":  "new york",
	"pages":  1,
	"country":  "www",
	"distance": "10",
	"date" : "D,
}
```
### GET (return)
The API will return an JSON object with array of objects containing each job posting as an object. 
Each job lisiting object contains: key <sup>[1]</sup>, title <sup>[2]</sup>, company <sup>[3]</sup>, location <sup>[4]</sup>, type <sup>[5]</sup>, salary <sup>[6]</sup>, job link <sup>[7]</sup>, summary <sup>[8]</sup> and date <sup>[9]</sup>.

 - [1] key: unique key for each job listing object
 - [2] title: job listing title
 - [3] company: company who posted the listing
 - [4] location: location of the positing
 - [5] type: full time or part time (when not mentioned on the posting, it might return the salary)
 - [6] salary: Salary if mentioned or else empty string
 - [7] job link: job link for the positing
 - [8] summary: few summary points mentioned on the card
 - [9] date: when it was posted such as 1 day ago, 2 days ago, 30+ days,..

ex: 
```
{
"result": [
	{
		"key": 1,
		"title":"Bread Baker",
		"company":"Forno Cultura",
		"location": "Toronto, ON",
		"type":"full-time",
		"salary": "$42,000–$48,000 a year",
		"date":"",
		"jobLink":"https://ca.indeed.com/viewjob?jk=2bf8b793b6662d31"
	}, 
	{
		"key": 2,
		"title":"Baker",
		"company":""Phipps Desserts"",
		"location": "Toronto, ON",
		"type":"full-time",
		"salary": "From $16.50 an hour",
		"date": "4 days ago",
		"jobLink":"https://ca.indeed.com/viewjob?jk=621fb0c19055bb94"
	},
	...

]
}
```
![image](https://user-images.githubusercontent.com/83378929/175841388-fbfbef12-c083-4395-ab60-362fbcb28aed.png)
