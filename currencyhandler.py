import json
from datetime import datetime
from typing import Any

import requests


class CurrencyHandler:
    def __init__(self, base_currency: str = "USD"):
        # You can only use "usd" as base in the API when using free tier.
        # Feel free to add more parameters if you have ideas on how
        # the class might benefit from that, making it more customizable.
        """
        Initialize the CurrencyHandler.

        This constructor should:
        1. Attempt to load currency data from a JSON file using the load_currency_data method.
        2. If no JSON data is found or if it's outdated, fetch new data from the exchangerates API using the fetch_currency_data method.
        3. Initialize any necessary instance variables for storing currency data and API information.

        # ADVICE: Start implementing the fetch_currency_data method
        """
        self.app_id = "f33364a5d1c040b6b44597e443dfc1f4"
        self.latest_api_url = (
            f"https://openexchangerates.org/api/latest.json?app_id={self.app_id}"
        )
        self.currency_api_url = f"https://openexchangerates.org/api/currencies.json?prettyprint=false&show_alternative=false&show_inactive=false&app_id={self.app_id}"
        self.base_currency = base_currency
        self.get_fetch_data = self.fetch_currency_data()
        self.tuples_list = []
        self.currency_log_data = []

    def fetch_currency_data(self) -> dict[str, Any]:
        """
        Fetch the latest currency exchange rate data from the openexchangerates API.

        This method should:
        1. Make an API request to fetch the latest exchange rates.
        2. Parse the JSON response and extract relevant data.
        3. Store the fetched data in the appropriate instance variable(s).
        4. Handle any potential errors or exceptions that may occur during the API request.

        Returns:
            A dictionary containing the latest exchange rates and metadata.
        """
        headers = {"accept": "application/json"}
        response = requests.get(self.latest_api_url, headers=headers)

        try:
            fetch_data = response.json()
        except ConnectionError:
            raise ConnectionError("Failed to connect to server.")
        except TimeoutError:
            raise TimeoutError("Server timed out error.")

        return fetch_data

    def convert_from_usd(self, amount: float, target_currency: str) -> float:
        """
        Convert a given amount from USD to another specified currency.
        This does not require you to use a "base" in the API, it can be done using basic math.

        Args:
            to_currency: The 3-letter code of the currency to convert to.
            amount: The amount in USD to be converted.

        Returns:
            The converted amount in the specified currency.

        Raises:
            ValueError: If the currency code is invalid or the amount is negative.
        """

        rate_data = self.fetch_currency_data()

        rates = rate_data.get("rates", {})

        if target_currency not in rates:
            raise ValueError(f"Currency '{target_currency}' not found in rate data.")

        rate = rates[target_currency]
        rate_converter_data = amount * rate

        return rate_converter_data

    def convert_any_currency(
        self, from_currency: str, to_currency: str, amount: float
    ) -> float:
        """
        Convert an amount from one currency to another using the latest exchange rates.

        Args:
            from_currency: The 3-letter code of the currency to convert from.
            to_currency: The 3-letter code of the currency to convert to.
            amount: The amount to be converted.

        Returns:
            The converted amount in the target currency.

        Raises:
            ValueError: If either currency code is invalid or the amount is negative.
        """

        self.from_currency = from_currency
        self.to_currency = to_currency
        self.amount = amount

        rate_converter_to_from_data = self.fetch_currency_data()

        rates = rate_converter_to_from_data.get("rates", {})

        if from_currency not in rates or to_currency not in rates:
            raise ValueError("The currency code you selected is not in our database.")

        usd_amount = amount / rates[from_currency]
        converted_amount = usd_amount * rates[to_currency]

        return converted_amount

    def list_currencies(self) -> list[str]:
        """
        List all available currencies in alphabetical order.
        # BONUS - somehow get the full currency names, and include that as well. Feel free to do it any way you like.

        Returns:
            A sorted list of available currency codes.
        """

        headers = {"accept": "application/json"}
        response = requests.get(self.currency_api_url, headers=headers)

        try:
            currency_data = response.json()
            for rate, complete_currency_name in currency_data.items():
                print(f"{rate}: {complete_currency_name}")
        except ConnectionError:
            raise ConnectionError("Failed to connect to server.")
        except TimeoutError:
            raise TimeoutError("Server timed out error.")

    def load_currency_data(
        self, get_fetch_data: list[dict[str:Any]] = None
    ) -> dict[str, Any]:
        """
        Load currency data from a JSON file.

        This method should:
        1. Check if a JSON file with saved currency data exists.
        2. If it exists, read and parse the JSON data.
        3. Check the timestamp of the saved data.
        4. If the data is older than one hour, call fetch_currency_data to update it.
        5. If no file exists or there's an error reading it, call fetch_currency_data.

        Returns:
            A dictionary containing the loaded (or fetched) currency data.
        """

        if get_fetch_data == None:
            self.get_fetch_data = []
        else:
            self.get_fetch_data = get_fetch_data

    def export_to_json(self) -> None:
        """
        Export the current currency data (for the latest currencies) to a JSON file.

        This method should:
        1. Convert the current currency data into a JSON-formatted string.
        2. Write the JSON data to a file, including the current timestamp.
        3. Handle potential errors that may occur during file writing.

        Raises:
            IOError: If there's an error writing to the file, or a custom exception.
        #"""
        timestamp_data = self.fetch_currency_data()
        timestamp_data["timestamp"] = datetime.now().isoformat()

        with open("currency_log.json", "w", encoding="utf-8") as f:
            json.dump(timestamp_data, f, ensure_ascii=False, indent=4)

    def get_historical_rate(self, date: str, base_currency: str) -> dict[str, Any]:
        """
        Get the historical exchange rate for a specific date using
        one of the relevant API-endpoints.

        Args:
            date: Date in YYYY-MM-DD format
            base_currency: 3-letter currency code to fetch historical rates based on

        Returns:
            The historical exchange rates as a dictionary for a specific date
            You should probably store it in a list or dict.
        """
        self.base_currency = base_currency
        self.date = date
        url = f"https://openexchangerates.org/api/historical/{self.date}.json?app_id={self.app_id}&base=USD&symbols={self.base_currency}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        try:
            historical_rate_data = response.json()
        except ConnectionError:
            print("Failed to connect to server.")
        except TimeoutError:
            print("Server timed out error.")

        return historical_rate_data

    def list_historical_rates_for_currency(
        self, currency: str, days: int
    ) -> list[tuple[str, str]]:
        """
        Get the trend of exchange rates for a currency over a specified number of days.

        Args:
            currency: 3-letter currency code
            days: Number of days to look back

        Returns:
            A list of tuples, each containing a date and the corresponding rate
            Tuples are typically used to store pairs of values.
        """
        self.currency = currency
        self.days = days
        url = f"https://openexchangerates.org/api/historical/{self.days}.json?app_id={self.app_id}&base=USD&symbols={self.currency}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        try:
            list_of_historical_rate_data = response.json()
        except ConnectionError:
            raise ConnectionError("Failed to connect to server.")
        except TimeoutError:
            raise TimeoutError("Server timed out error.")

        return list_of_historical_rate_data
