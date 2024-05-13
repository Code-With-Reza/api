import json
import datetime

def get_country(data, param):
    with open('lib/country_data.json', 'r') as file:
        country_data = json.load(file)

    result = {
        "status": 200,
        "message": "success",
        "result": {}
    }

    if data == "code":
        country = next((country for country in country_data if country["country_code"] == param or country["three_letter_country_code"] == param), None)
    elif data == "phone":
        country = next((country for country in country_data if country["phone_code"] == param or "+" + country["phone_code"] == param), None)
    elif data == "name":
        country = next((country for country in country_data if country["country_name"] == param), None)
    elif data == "currency":
        country = next((country for country in country_data if country["currency_code"] == param), None)
    else:
        result["status"] = 400
        result["message"] = "Invalid data parameter"
        return json.dumps(result, indent=4, ensure_ascii=False)

    if country:
        result["result"]["name"] = country["country_name"]
        result["result"]["alpha2Code"] = country["country_code"]
        result["result"]["alpha3Code"] = country["three_letter_country_code"]
        result["result"]["callingCodes"] = [country["phone_code"]]
        result["result"]["capital"] = country["capital_name"]
        result["result"]["region"] = country["continent_name"]
    else:
        result["status"] = 404
        result["message"] = "Country not found"

    return json.dumps(result, indent=4, ensure_ascii=False)



def get_countdown(day, month=None, year=None):
    try:
        # Check if all parameters are provided
        if month is None or year is None:
            raise ValueError("All date parameters (day, month, year) must be provided")

        # Convert parameters to integers
        day = int(day)
        month = int(month)
        year = int(year)

        # Validate date
        target_date = datetime.datetime(year, month, day)
        current_date = datetime.datetime.now()
        
        remaining_time = target_date - current_date
        
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        result = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        
        response = {
            "status": 200,
            "message": "success",
            "result": result
        }
        
        return json.dumps(response, indent=4, ensure_ascii=False)
    except (ValueError, TypeError) as e:
        # Handle incorrect parameters or non-integer inputs
        response = {
            "status": 500,
            "message": "error",
            "result": str(e)
        }
        
        return json.dumps(response, indent=4, ensure_ascii=False)