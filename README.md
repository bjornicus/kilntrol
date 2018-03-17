# kilntrol
Raspberry pi automatic kiln controller and graphical viewer.

`upload_logs.py`Logs temperature readings to a google spreadsheet.  Requires google api python client:
`pip install --upgrade google-api-python-client`

When running on the raspberry pi use `python upload_logs.py --noauth_local_webserver` to start.
