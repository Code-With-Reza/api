import requests
import re
import json

def get_apk(package_name, debug=0):
    if package_name is None:
        return
    # Specify user agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Make request to the API with specified headers
    api_url = f"https://apk-dl.com/{package_name}"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        resp = {"status": response.status_code, "message": "Error occurred while fetching data"}
    if debug == 1:
        print("We are in!")
    # Extracting data using regular expressions
    data = response.text

    # Get icon image source
    icon_pattern = r'<div class="logo"> <img src="([^"]+)"'
    icon_match = re.search(icon_pattern, data)
    icon_url = icon_match.group(1) if icon_match else None
    if debug == 1:
        print("got icon")
    
    # Get apk name
    name_pattern = r'<div class="title">App Name</div> <div>([^<]+)</div>'
    name_match = re.search(name_pattern, data)
    apk_name = name_match.group(1).strip() if name_match else None
    if debug == 1:
        print("got name")
    
    # Get apk version
    version_pattern = r'<div class="title">Version</div> <div>([^<]+)</div>'
    version_match = re.search(version_pattern, data)
    apk_version = version_match.group(1).strip() if version_match else None
    if debug == 1:
        print("got version")
    
    # Get apk author
    author_pattern = r'<div class="title">Developer</div> <div>([^<]+)</div>'
    author_match = re.search(author_pattern, data)
    apk_author = author_match.group(1).strip() if author_match else None
    if debug == 1:
        print("got author")
    
    # Get apk download link
    link_pattern = r'<a rel="nofollow" class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored" href="([^"]+)"'
    link_match = re.search(link_pattern, data)
    apk_link = link_match.group(1) if link_match else None
    if debug == 1:
        print("got link 1")
    
    # Requesting the first link to get the final download link
    if apk_link:
        link_response = requests.get("https://apk-dl.com/"+apk_link, headers=headers)
        if link_response.status_code == 200:
            # Get apk download link
            link_pattern = r'<a rel="nofollow" href="([^"]+)" title="'
            link_match = re.search(link_pattern, link_response.text)
            apk_link2 = link_match.group(0) if link_match else None
            apk_link2 = apk_link2.replace('<a rel="nofollow" href="','')
            apk_link2 = apk_link2.replace('" title="','')
            if debug == 1:
                print("got link 2")
            resp = {
        "status": 200,
        "message": "success",
        "result": {
            "apk_name": apk_name,
            "apk_icon": icon_url,
            "apk_version": apk_version,
            "apk_author": apk_author,
            "apk_link": apk_link2 + "&dl=2"
        }}
    
    else:
        resp = {"status": 404, "message": "Data not found"}
    return json.dumps(resp, indent=4, ensure_ascii=False)
