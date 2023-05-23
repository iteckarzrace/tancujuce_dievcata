#!/usr/bin/python3
import requests
import csv
from twocaptcha import TwoCaptcha
import configparser
import random

# Read the config file
config = configparser.ConfigParser()
config.read('config.ini')

# Get the configuration values
api_key = config.get('API', 'api_key')
urlAjax = config.get('URL', 'urlAjax')
csv_file = config.get('CSV', 'csv_file')
sitekey = config.get('RECAPTCHA', 'sitekey')
captcha_url = config.get('RECAPTCHA', 'captchaUrl')
output_csv_file = config.get('CSV', 'output_csv_file')

# Instantiate the TwoCaptcha client with your API key
solver = TwoCaptcha(api_key)

# Function to parse the response and search for multiple strings
def parse_response(response, target_strings):
    for target_string, result in target_strings.items():
        if target_string in response:
            return result

    return "Something went wrong!"

# Function to generate a random user agent
def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.50",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.50",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
        # Add more user agent strings as needed
    ]

    return random.choice(user_agents)

try:
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['vote_result']

        with open(output_csv_file, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                # Define the data to be posted
                data = {
                    'totalpoll[choices][0a31fc29-13d9-4aa9-aafc-e4b0dd97754e][]': '87e8015e-9cb1-4072-b4c9-c99eaa1eb10b',
                    'totalpoll[screen]': 'vote',
                    'totalpoll[pollId]': '225',
                    'totalpoll[action]': 'vote',
                    'totalpoll[fields][firstname]': row['first_name'],
                    'totalpoll[fields][lastname]': row['last_name'],
                    'totalpoll[fields][email]': row['email_address'],
                }

                # Solve the reCAPTCHA using 2captcha
                result = solver.recaptcha(
                    sitekey=sitekey,
                    url=captcha_url
                )

                # Retrieve the solved CAPTCHA response
                captcha_response = result['code']

                # Add the solved CAPTCHA response to the data
                data['g-recaptcha-response'] = captcha_response

                # Generate a random user agent
                user_agent = get_random_user_agent()

                # Set the user agent in the request headers
                headers = {'User-Agent': user_agent}

                # Make the POST request with the updated data and headers
                response = requests.post(urlAjax, data=data, headers=headers)

                # Define the target strings and corresponding results
                target_strings = {
                    "Email bolo už použité.": "EmailUsed - NOK",
                    "Ďakujeme za váš hlas!": "Voted - OK",
                    # Add more target strings and results as needed
                }

                # Parse the response and search for the target strings
                vote_result = parse_response(response.text, target_strings)

                # Write the row to the output CSV file with the vote_result
                row['vote_result'] = vote_result
                writer.writerow(row)

                # Print the processed row
                print(f"Processed Row: {row}")

                # Check if the response is "Something went wrong"
                if vote_result == "Something went wrong!":
                    print("Error: Something went wrong in the response. Stopping further calls.")
                    break

except Exception as e:
    print(f"Error solving reCAPTCHA: {str(e)}")
