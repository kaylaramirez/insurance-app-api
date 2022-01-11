# insurance-app-api
Take home challenge

## About
Project for creating and checking out Volcano Insurance.

This project has two endpoints and it uses TokenAuthentication. User must be authenticated to make both requests.
You can createasuperuser then assign it a token to user.

## Endpoints

### Create a Quote
POST: /api/quote/CREATE/

Payload = {
"effective_data": null,
"previous_policy_cancelled": true,
"miles_to_volcano": 25,
"property_owner": true,
"address": {
   "id": 2,
   "street_address_1": "2909 Santa Lucia St",
   "street_address_2": "",
   "city": "Corpus Christi",
   "state": "TX",
   "zipcode": "78415"
}

### Checkout a quote
GET: /api/quote/{{quote_id}}/

Response = {
    "id": 2,
    "quote_id": "9MJ66UKEFA",
    "term_premium": 107.892,
    "monthly_premium": 17.982,
    "total_fees": 59.94,
    "monthly_fees": 9.99,
    "total_discounts": 11.988,
    "monthly_discounts": 1.998
}

### Disclaimer:
I am fully aware that this does not have 100% test cover. I could not for the life of me get coverage or django-nose to run locally. I just wanted y'all to know that I am aware. A couple of other things I know can be improved on. Address model can use better validation. I found a few packages that could have been nice to implement if time permitted. I debated a while to about how much to round, I landed on hundreth for testing but I would have asked for requirement clarification. Address isn't storing user which I think it should. There are for sure other things I missed but that's all I got for now. Thank you for the oppportunity! This was fun.


## LOCAL Development
This project is wired up to work with Docker. You aren't required to use it, 
but it can make things easier. The instructions in the next sections will 
include instructions for both Docker

### Running the Server

Setup:
   a. Run `docker-compose build` inside your local repo (if not already built)
   b. Run `docker-compose run`

### Running Test and Linting Code
- Run `docker-compose run --rm app sh -c "python manage.py test && flake8"`
  - This project uses Travis CL 

### Running a django command
- Run `docker-compose run --rm app sh -c "<command to run>"` 
  - ex: `docker-compose run --rm app sh -c makemigrations` 
