# gal-career-partners
Kristen's pet project


Script for pulling LinkedIn contact data (Name & URl) from a specifced companies page. Script flow:

1. open li, login with creds
2. click global search bar
3. input co name
4. click people
5. input search keyword
    Gal alum: `'galvanize'`
    Tech Recruiter: `'technical recruiter'` & `'Austin, TX Area'`
6. scroll to bottom of page
7. scrape contact profiles that are populated
8. load each company scrape into mongodb
-  company name as `k`, `dict` of contact name (`k`) and url (`v`) as v