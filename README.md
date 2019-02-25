# localinfo
Get local weather and news based on your IP

### How to make requests to backend using httpie ###

How to request info about IP:

`http POST http://<server>:8000/ips/ number='174.114.56.169'`

    HTTP/1.1 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Length: 305
    Content-Type: application/json
    Date: Sun, 24 Feb 2019 22:38:07 GMT
    Server: WSGIServer/0.2 CPython/3.6.5
    Vary: Accept, Cookie
    X-Frame-Options: SAMEORIGIN

    {
        "city": "Ottawa",
        "country_flag": "http://assets.ipstack.com/flags/ca.svg",
        "country_name": "Canada",
        "id": 2,
        "latitude": "45.4289",
        "longitude": "-75.6844",
        "number": "174.114.56.169",
        "region_name": "Ontario",
        "weather": {
            "description": "Light rain",
            "humidity": 86,
            "pressure": 984,
            "temperature": 276.64,
            "wind_speed": 11.8
        },
        "news": [{
            "author": "Amy Forliti",
            "content": "Actor Terrence Howard, who plays the father of Jussie Smollett's character on \"Empire,\" has expressed support for his fellow cast member amid allegations that Smollett staged a racist, anti-gay attack on himself. Howard, who plays music mogul Lucious Lyon on … [+1876 chars]",
            "description": "Actor Terrence Howard, who plays the father of Jussie Smollett's character on \"Empire,\" has expressed support for his fellow cast member amid allegations that Smollett staged a racist, anti-gay attack on himself.",
            "publishedAt": "2019-02-24T21:55:00Z",
            "source": {
                "id": null,
                "name": "Cp24.com"
            },
            "title": "'Empire' star Terrence Howard shows support for Jussie Smollett - CP24 Toronto's Breaking News",
            "url": "https://www.cp24.com/entertainment-news/celebrity-news/empire-star-terrence-howard-shows-support-for-jussie-smollett-1.4310411",
            "urlToImage": "https://www.cp24.com/polopoly_fs/1.4310415.1551038933!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg"
        }...]
    }

View list of already saved IPs:

`http http://<server>:8000/ips/`

    HTTP/1.1 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Length: 399
    Content-Type: application/json
    Date: Sun, 24 Feb 2019 22:38:47 GMT
    Server: WSGIServer/0.2 CPython/3.6.5
    Vary: Accept, Cookie
    X-Frame-Options: SAMEORIGIN

    [
        {
            "city": "Ottawa",
            "country_flag": "http://assets.ipstack.com/flags/ca.svg",
            "country_name": "Canada",
            "id": 1,
            "latitude": "45.4289",
            "longitude": "-75.6844",
            "number": "174.114.56.169",
            "region_name": "Ontario"
        },
        {
            "city": "Ottawa",
            "country_flag": "http://assets.ipstack.com/flags/ca.svg",
            "country_name": "Canada",
            "id": 2,
            "latitude": "45.4289",
            "longitude": "-75.6844",
            "number": "174.114.56.170",
            "region_name": "Ontario"
        }
    ]

View complete info about location:

`http http://<server>:8000/ips/2/`

    HTTP/1.1 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Length: 305
    Content-Type: application/json
    Date: Sun, 24 Feb 2019 22:43:28 GMT
    Server: WSGIServer/0.2 CPython/3.6.5
    Vary: Accept, Cookie
    X-Frame-Options: SAMEORIGIN

    {
        "city": "Ottawa",
        "country_flag": "http://assets.ipstack.com/flags/ca.svg",
        "country_name": "Canada",
        "id": 2,
        "latitude": "45.4289",
        "longitude": "-75.6844",
        "number": "174.114.56.170",
        "region_name": "Ontario",
        "weather": {
            "description": "Light rain",
            "humidity": 86,
            "pressure": 984,
            "temperature": 276.64,
            "wind_speed": 11.8
        },
        "news": [{
            "author": "Amy Forliti",
            "content": "Actor Terrence Howard, who plays the father of Jussie Smollett's character on \"Empire,\" has expressed support for his fellow cast member amid allegations that Smollett staged a racist, anti-gay attack on himself. Howard, who plays music mogul Lucious Lyon on … [+1876 chars]",
            "description": "Actor Terrence Howard, who plays the father of Jussie Smollett's character on \"Empire,\" has expressed support for his fellow cast member amid allegations that Smollett staged a racist, anti-gay attack on himself.",
            "publishedAt": "2019-02-24T21:55:00Z",
            "source": {
                "id": null,
                "name": "Cp24.com"
            },
            "title": "'Empire' star Terrence Howard shows support for Jussie Smollett - CP24 Toronto's Breaking News",
            "url": "https://www.cp24.com/entertainment-news/celebrity-news/empire-star-terrence-howard-shows-support-for-jussie-smollett-1.4310411",
            "urlToImage": "https://www.cp24.com/polopoly_fs/1.4310415.1551038933!/httpImage/image.jpg_gen/derivatives/landscape_620/image.jpg"
        }...]
    }


### List of things to improve in future ###

- Use production server instead of Django development server
- Restrict number of requests per minute to avoid bot attacks
- Implement pagination both for frontend and DB queries
- Handle external APIs timeouts and retries
- Better handle of data errors from external APIs (use custom exceptions)
- Tested only on IPv4 numbers, add support for IPv6
- Right now it checks that IP is valid but ideally should allow only public IPs
- More tests (had problem with mocking Redis)
