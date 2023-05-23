# Pozdrav pre Lubosa v plavkach🤓! 👙

This script automates the process of submitting votes using the TotalPoll Pro WordPress plugin. It solves the reCAPTCHA challenge and submits votes based on the provided data.

## Dependencies

To run this script, you need to have the following dependencies installed:

- Python 3.6 or above
- 2captcha-python library (can be installed via `pip3 install 2captcha-python`)

## Configuration

Before running the script, you need to provide the necessary configuration properties. Follow the steps below:

1. Create a configuration file named `config.ini`.
2. Open the `config.ini` file in a text editor and fill in the following properties:

```ini
[API]
api_key = <your_2captcha_api_key>

[URL]
urlAjax = <admin_ajax_url>

[CSV]
csv_file = <path_to_input_csv_file>
output_csv_file = <path_to_output_csv_file>

[RECAPTCHA]
sitekey = <reCAPTCHA_site_key>
captchaUrl = <captcha_solve_url>
```

* `api_key`: Your 2Captcha API key.
* `urlAjax`: The URL for the TotalPoll Pro voting endpoint (admin-ajax.php).
* `csv_file`: The path to the input CSV file containing the voting data.
* `output_csv_file`: The path to the output CSV file where the results will be saved.
* `sitekey`: The reCAPTCHA site key for the voting page.
* `captchaUrl`: The URL to solve the reCAPTCHA challenge.

## Running the Script
To run the script, follow these steps:

1. Make sure you have installed Python 3.6 or above.
2. Install the required dependencies by running pip3 install 2captcha-python.
3. Fill in the configuration properties in the config.ini file.
4. Place your input CSV file in the specified location.
5. Open a terminal or command prompt and navigate to the script directory.
6. Run the script using the following command:
```
python3 script.py
```
7. The script will start processing the votes and output the processed rows. The results will be saved to the specified output CSV file.

## Notes
* The script will automatically solve the reCAPTCHA challenge using the 2captcha API.
* If the response from the website contains any of the target strings defined in the script, the corresponding result will be saved in the vote_result column of the output CSV file.
* If the response contains "Something went wrong", the script will stop further calls and display an error message.
* Feel free to modify the script according to your specific use case and requirements.
* 🚨**There is a limit of 10 votes per IP per day!!! Script currently doesn't handle rotation via HTTP PROXY.**🚨

Feel free to modify the script according to your specific use case and requirements.

If you encounter any issues or have any questions, please open an issue in this repository.


Make sure to replace `<your_2captcha_api_key>`, `<admin_ajax_url>`, `<path_to_input_csv_file>`, `<path_to_output_csv_file>`, `<reCAPTCHA_site_key>`, and `<captcha_solve_url>` with the actual values specific to your setup.

You can place this markdown content in a file named `README.md` in the root directory of your GitHub repository.
