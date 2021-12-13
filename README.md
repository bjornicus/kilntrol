# kilntrol
Raspberry pi automatic kiln controller and graphical viewer (via google sheets).

Uploading to google sheets requires google api python client:
`pip install --upgrade google-api-python-client`

Start the controller and log uploader by running `./start`

# Requirements
You'll need 
- a kiln
- a raspberry pi with python 3.10 [installed](https://itheo.tech/installing-python-3-10-on-raspberry-pi/)
- a type K thermocouple
- a [MAX31855 breakout board](https://www.adafruit.com/product/269) for reading the thermocouple. Here's some additional [useful reading](https://learn.adafruit.com/thermocouple) on that.
- a relay capable of switching whatever voltage and current your kiln needs 
