<h1 align="center">Bet Web Scraper</h1>

<p align="center">A python script that scrapes the <a href="https://www.ufc.com/events">UFC Website</a> and uploads the results to a Google Firebase Realtime Database</p>

## Links

- [Web Scraper Repo](https://github.com/khoi-h-tran/Bet-Backend "Web Scraper Repo")

## Screenshots

### Static web scraping (using BeautifulSoup4) - finds the next upcoming event and pulls all relevant event info
![image](https://user-images.githubusercontent.com/59266614/187511060-40fbdf90-1a37-45c5-9c1a-b4ac704a58f7.png)

### Dyanmic web scraping (using Selenium) - clicks on the next event and pulls all relevant figher info
![image](https://user-images.githubusercontent.com/59266614/187512427-aed1df17-c2df-4c58-9660-0e580898f9a6.png)

### Dyanmic web scraping (using Selenium) - clicks on each match-up and pulls the fighter records
![image](https://user-images.githubusercontent.com/59266614/187512712-2296b949-6b4c-45c9-b249-5825ad680ae2.png)

### Script serializes the scraped data (using Marshmallow) and sends the JSON to Firebase Realtime Database

| Sample Database Images   |
|----------|
| Saving Event Info (e.g. Date, Arena, etc.) |
| ![image](https://user-images.githubusercontent.com/59266614/187514534-2723fc4c-3459-4055-8278-265064104cbe.png) |
| Saving Card Info |
| ![image](https://user-images.githubusercontent.com/59266614/187514446-a8fe2ae6-f7f8-41b3-8f16-53be1186443a.png) |
| Saving Fighter Info (e.g. Fighter Names, Images, Records, etc.) |
| ![image](https://user-images.githubusercontent.com/59266614/187514278-73756e0f-a829-4a8f-ba91-a8c5f7f2517b.png) |

## Built With

- Python
- BeautifulSoup4 (Static Web Scraper)
- Selenium (Dyanmic Web Scraper)
- Marshmallow (Python Library for Class Serialization)
- Firebase Real Time Database

## Future Updates

- [ ] Regularly Scheduled Web Scraping
- [ ] Add scraping of event results (winners, losers, etc.)
- [ ] Add bet results (check if users bet on correct fighers)
- [ ] Add statistics (display bet performance for users on the front-end)

## Author

**Khoi Tran**

- [Profile](https://github.com/khoi-h-tran "Khoi Tran")
- [Email](mailto:khoi.huynh.tran@gmail.com?subject=GitHubReadMe "Hi!")

## 🤝 Support

Give a ⭐️ if you like this project!
