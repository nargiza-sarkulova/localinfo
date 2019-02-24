# localinfo
Get local weather and news based on your IP

### How to make requests to backend using httpie ###

How to request info about IP:

`http POST http://<server>:8000/ips/ number='174.114.56.169'`

View complete info about location:

`http http://<server>:8000/ips/<pk>/`


### List of things to improve in future ###

- Use production server instead of Django development server
- Restrict number of requests per minute to avoid bot attacks
- Implement pagination both for frontend and DB queries
- Handle external APIs timeouts and retries
- Better handle of data errors from external APIs (use custom exceptions)
- Tested only on IPv4 numbers, add support for IPv6
- Right now it checks that IP is valid but ideally should allow only public IPs
- More tests (had problem with mocking Redis)
