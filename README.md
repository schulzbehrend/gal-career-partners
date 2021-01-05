The job search for anyone, post-immersive program, following a traditional graduation route, or post canning is a grueling one. LinkedIn is the leading source of networking, integrating job search tools and recruiters into its platform who could say no to the resources freely available? Certainly not anyone who’s looking for a profession in a timely manner. LinkedIn provides __global access__ to companies and professionals in any and every field imaginable.
But where does one start? [LinkedIn](https://about.linkedin.com/) boasts an astonding 722+ million members across 200 countries. It’s more than a full time job to network through the labrythn of laborous professionals, who have their own agenda, motives, initiatives, and, above all, families, that they too are working into a 40-hour work week. How does one tap into the extensive networking power that LinkedIn holds with the prowess of a data scientist?
This repository aims to do exactly that by utilizing the main question one asks oneself at the start of a job hunt, ‘Where do I want to work?’
Starting with a simple list of companies to search the scripts in this repo scrapes Galvanize Alumni contacts and Technical Recruiters from a specified company into a Mongo DB for fast networking.
- Script for pulling LinkedIn contact data (Name & URL) from list of companies specified in `companies.py`
- ### Prerequists and dependencies
    1. `data/LI_login.txt` save structure
- Script flow for **technical recruiters** and **galvanize alumni**
    1. Create `panda.Series` object from company list in `companies.py`
    2. Open LinkedIn with credentials from `data/LI_login.txt`
    3. `.apply()` on company `pandas.Series` object
        1. Select global search bar on LinkedIn
        2. Input company name
        3. Input search keyword
            - **Galvanize Alumni:** `galvanize`
            - **Technical Recruiter:** `technical recruiter` + `Austin, TX Area`
        4. Scroll the bottom of the page to complete lazy load of LinkedIn Member search results
        5. Scrape contact ID cards
        6. Load each company search result in the MongoDB
            - `Dictionary` structured `{‘companyname1’: {‘contact1’:’url1’, ‘contact2’:’url2’, ...}}`
- ## Images
    - {{[[TODO]]}} tech stack
    - {{[[DONE]]}} Galvanize logo
- # Team
    - [[Justin Wallander]]
