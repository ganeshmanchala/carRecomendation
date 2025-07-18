﻿# carRecommendation
ABSTRACT

The car market offers automobile consumers a dilemma of many choices since the existing process does not have a solution to effectively match individual needs. The project formulates the Car Suggestion System that integrates adaptive web scraping techniques with ranking algorithms based on machine learning for the solution. A friendly interface allows users to expose their requirements in terms of budget as well as seating needs and fuel type preferences and this triggers a two-step backend process. A scraper ensemble of Selenium and BeautifulSoup fetches up-to-date car specs directly from auto websites. APScheduler runs on a daily basis to schedule data update which maintains MongoDB databases up-to-date as both of them get clean and normalized data storage.

LightGBM ranking models are the primary elements of the system since they rank electric car data independently from fuel-based automobile data through the utilization of numerous features such as price and mileage and user behavioral patterns. Rule-based filters function as a pre-screening operation that involves using set rules (safety rating specifications) before employing collaborative ranking to determine rankings for vehicles. Analysis via user queries displayed an 80% success rate in recognizing user preferences that reduced the length of searches. A scalable system is integrated into dealership platforms via a JWT-secured Flask API so that it provides solutions for data-driven auto decision-making and automotive platform integration and rental services.  

Software Requirements

Frontend (React App):
•	Framework: React v18+ + React Router v6 for routing.  
•	React state or Redux for user sessions and car recommendation states. 
•	UI Library: Material-UI (MUI) v5 | Ant Design for pre-built components (table, forms, modals)  
•	Authentication: JSON Web Tokens (JWT) — Secure user login/signup flows 
•	HTTP Client: Axios v1. 3+ for the API calls to the Flask backend. 
•	Build Tools: Node.js v16+, npm  for dependencies management. 


Backend (Flask API):
•	Programming Language: Python 3.9+ using Flask v2. 2+ along with Flask-RESTful for the API endpoints. 
•	Database: MongoDB v6. From 0+ using PyMongo driver for the CRUD operations.
•	Scraping: Selenium v4. ChromeDriver for scraping JavaScript websites, BeautifulSoup4 for HTML parsing. 
•	Scheduling: APScheduler v3. 10+ for automatic daily updates of data. 
•	ML Integration: LightGBM v3. for ranking models, Pickle: For model serialization 3+ 
•	Authentication: Flask-JWT-Extended v4 4+ for token-based access control. 



Implementation Images:
![image](https://github.com/user-attachments/assets/c2b8af61-31ca-4356-95f2-5b4d6a14180d)
![image](https://github.com/user-attachments/assets/635382ee-89fa-45ba-b86c-e3627c91f8a2)
![image](https://github.com/user-attachments/assets/168bc9a7-d57c-4c1e-afda-93f1fc9a1a86)
![image](https://github.com/user-attachments/assets/6aae4bc2-c8cb-4244-b6ed-d9b33f66b6b3)
![image](https://github.com/user-attachments/assets/96c6a4a6-65a3-4e9f-9ab3-a7278a545e82)





