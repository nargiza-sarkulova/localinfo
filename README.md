# localinfo
Get local weather and news based on your IP

### How to make requests to backend using httpie ###

How to request info about IP:

`http POST http://<server>:8000/ips/ number='174.114.56.169'`

View complete info about location:

`http http://<server>:8000/ips/<pk>/`
