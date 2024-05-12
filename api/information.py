import json

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
