from datetime import datetime, timedelta
from typing import Any

import requests
from currencyhandler import CurrencyHandler

# DO NOT UPLOAD A VIRTUAL ENVIRONMENT TO GIT
# Add the name of your virtual environment to .gitignore
# Now you can git add and git commit.
# Remove the pass keyword from the method when you start implementing the method

# REMEMBER TO MAKE COMMITS FREQUENTLY! I don't want to see only 1 commit with all the code in it.
# You can remove these comments^

# Think of the CurrencyHandler as a class that should strictly only handle functionality.
# Using print, input or similar should be done outside of the class, in such way
# that you COULD use the currencyhandler in any type of application that might
# want to use currencies


def main() -> None:
    """
    The main function that runs the currency conversion application.

    This function should:
    1. Create an instance of the CurrencyHandler class.
    2. Display a menu of options to the user.
    3. Handle user input and call the appropriate methods of the CurrencyHandler.
    4. Provide a loop to allow multiple operations in a single session.
    5. Handle any errors or exceptions that may occur during operation.

    Menu options should include:
    [0] - List all currencies
    [1] - Convert USD to a currency of choice
    [2] - Manually refresh the data (fetch new currency data)
    [3] - Export the data to JSON
    [4] - Convert from any currency to any currency
    [5] - Get historical exchange rate
    [6] - List historical rates for a currency + more
    [7] - Exit the application
    """
    # Use this instance of CurrencyHandler to do stuff in your menu.
    currency_handler = CurrencyHandler()

    while True:
        print("\nCurrency Converter Menu:")
        print("[0] - List all currencies")
        print("[1] - Convert USD to a currency of choice")
        print("[2] - Refresh the data (fetch new currency data)")
        print("[3] - Export the data to JSON")
        print("[4] - Convert from any currency to any currency")
        print("[5] - Get historical exchange rate")
        print("[6] - Get rate trend for a currency")
        print("[7] - Exit the application")
        print("")
        choice = input("Enter your choice (0-7): ")
        print("")

        if choice == "0":
            try:
                currency_handler.list_currencies()
            except ConnectionError:
                print(
                    "We have run in to a problem with the connection, please try again."
                )

        elif choice == "1":
            get_existing_currency = currency_handler.fetch_currency_data()

            selected_currency = str(
                input(
                    "Please select a currency by it's 3-letter code or press Q to go back: "
                ).upper()
            )
            while True:
                if selected_currency == "Q":
                    break
                elif selected_currency in get_existing_currency["rates"]:
                    selected_currency = selected_currency
                    break
                else:
                    selected_currency = str(
                        input(
                            "The currency code you selected is not in our database, please try again: "
                        ).upper()
                    )
            usd_amount = input(
                f"Enter the desired amount in USD to converted to {selected_currency}: "
            )
            while True:
                try:
                    usd_amount = float(usd_amount)
                    break
                except ValueError:
                    usd_amount = input(
                        "You need to enter a amount in digits, please try again: "
                    )

            usd_converter = currency_handler.convert_from_usd(
                amount=usd_amount, target_currency=selected_currency
            )
            usd_converter_calculation = usd_converter
            print("")
            print(f"Total in {selected_currency}: {usd_converter_calculation}")

        elif choice == "2":
            try:
                currency_handler.fetch_currency_data()
                print("Refresh complit.")
            except ConnectionError:
                print(
                    "We have run in to a problem with the connection, please try again."
                )

        elif choice == "3":
            currency_handler.export_to_json()
            print("Log is saved as currency_log.json")

        elif choice == "4":
            get_existing_currency = currency_handler.fetch_currency_data()

            while True:
                from_currency = str(
                    input(
                        "Please select the currency that you want to convert from, by it's 3-letter code or press Q to go back: "
                    ).upper()
                )
                if from_currency == "Q":
                    break
                elif from_currency in get_existing_currency["rates"]:
                    from_currency = from_currency
                    break
                else:
                    from_currency = str(
                        input(
                            "The currency code you selected is not in our database, please try again: "
                        ).upper()
                    )

            while True:
                to_currency = str(
                    input(
                        "Now you can choose the currency you want to change to, by it's 3-letter code or press Q to go back: "
                    ).upper()
                )
                if to_currency == "Q":
                    break
                elif to_currency in get_existing_currency["rates"]:
                    to_currency = to_currency
                    break
                else:
                    to_currency = str(
                        input(
                            "The currency code you selected is not in our database, please try again: "
                        ).upper()
                    )

            while True:
                try:
                    from_currency_amount = float(
                        input(f"Now add your desired amount for {from_currency}: ")
                    )
                    break
                except ValueError:
                    print("You need to add an amount.")
                    from_currency_amount = float(
                        input(
                            f"Please try again to add your desired amount for {from_currency}: "
                        )
                    )

            to_converter = currency_handler.convert_any_currency(
                from_currency=from_currency,
                to_currency=to_currency,
                amount=from_currency_amount,
            )
            converter_calculation = from_currency_amount * to_converter
            print("")
            print(
                f"Total amount of {from_currency} to {to_currency} is: {converter_calculation}"
            )

        elif choice == "5":
            get_existing_currency = currency_handler.fetch_currency_data()
            while True:
                desired_historical_rate = str(
                    input(
                        "Please select the currency that you want the historical rate from by it's 3-letter code or press Q to go back: "
                    ).upper()
                )
                if desired_historical_rate == "Q":
                    break
                elif desired_historical_rate in get_existing_currency["rates"]:
                    desired_historical_rate = desired_historical_rate
                    break
                else:
                    desired_historical_rate = str(
                        input(
                            "The currency code you selected is not in our database, please try again: "
                        ).upper()
                    )

            while True:
                historical_date = str(
                    input("Now please enter a desired date(YYYY-MM-DD): ").upper()
                )
                try:
                    historical_date = historical_date
                    break
                except TypeError:
                    historical_date = str(
                        input(
                            "The date is not in our database, please try again(YYYY-MM-DD): "
                        ).upper()
                    )

            completed_historical_value = currency_handler.get_historical_rate(
                date=historical_date, base_currency=desired_historical_rate
            )
            historical_rate = completed_historical_value.get("rates", {})
            historical_value = historical_rate.get(desired_historical_rate)
            print("")
            print(
                f"The rate for 1 USD in {desired_historical_rate}, at the date of {historical_date} was: {historical_value}"
            )

        elif choice == "6":
            get_existing_currency = currency_handler.fetch_currency_data()
            max_days = 14

            while True:
                desired_historical_rate = str(
                    input(
                        "Please select the currency that you want the historical rate from by it's 3-letter code or press Q to go back: "
                    ).upper()
                )
                if desired_historical_rate == "Q":
                    break
                elif desired_historical_rate in get_existing_currency["rates"]:
                    desired_historical_rate = desired_historical_rate
                    break
                else:
                    desired_historical_rate = str(
                        input(
                            "The currency code you selected is not in our database, please try again: "
                        ).upper()
                    )
            while True:
                historical_date = input(
                    "Now please enter a desired start date(YYYY-MM-DD): "
                )
                try:
                    starting_date = datetime.strptime(
                        historical_date, "%Y-%m-%d"
                    ).date()
                    break
                except TypeError:
                    print("The date is not in our database, please try again.")
                except ValueError:
                    print(
                        "The date you have enter is not a valed date, please try again."
                    )

            while True:
                number_of_days = int(input("How meny days do you want to log? "))
                if number_of_days <= max_days:
                    number_of_days = int(number_of_days)
                    break
                else:
                    print(
                        "The number of days you askt for in not valed, please try again."
                    )

            completed_historical_value = currency_handler.get_historical_rate(
                date=historical_date, base_currency=desired_historical_rate
            )
            historical_rate = completed_historical_value.get("rates", {})
            historical_value = historical_rate.get(desired_historical_rate)

            print("")
            print(f"The rate for 1 USD in {desired_historical_rate}:")
            for day in range(number_of_days + 1):
                date = starting_date + timedelta(days=day)
                print("")
                print(
                    date.strftime("%Y-%m-%d")
                    + f" - {desired_historical_rate}: {historical_value}"
                )

        elif choice == "7":
            print("Thank you for using the Currency Converter. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
