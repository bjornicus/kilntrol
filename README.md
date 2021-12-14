# kilntrol
Raspberry pi automatic kiln controller and graphical viewer (via google sheets).

Uploading to google sheets requires google api python client:
`pip install --upgrade google-api-python-client`

Start the controller and log uploader by running `./start`

# Requirements
For kilntrol you'll need:
- a kiln
- a raspberry pi with python >= 3.6
- a type K thermocouple
- a [MAX31855 breakout board](https://www.adafruit.com/product/269) for reading the thermocouple. Here's some additional [useful reading](https://learn.adafruit.com/thermocouple) on that.
- a relay capable of switching whatever voltage and current your kiln needs 

For uploading temperature logs to google sheets you'll need:
- The dependecies installed: `pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

