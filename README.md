# YellowBlink

A tiny server based on [Bottle](https://bottlepy.org/docs/dev/) to set up a webradio alarm clock on a Raspberry Pi. This project was inspired by [Piclodio](https://github.com/Sispheor/piclodio3), but it is written from scratch.

## Usage

Run `LungFish.py` and access [`http://localhost:8080/home`](http://localhost:8080/home) with a web browser. To deploy on your local network, change the last two lines of `LungFish.py` to:

```python
# run( host='localhost', port=8080, debug = True )
run( host='0.0.0.0', port=8080, debug = False )
```
## Dependencies

Tested on Debian and Raspberry Pi OS (Bullseye).


```
apt-get install mplayer python3-alsaaudio python3-crontab python3-pip
```
```
pip install bottle
```
## Default sound card

Edit `/usr/share/alsa/alsa.conf` and change `0` to `1` in the following lines:
```
defaults.ctl.card 0
defaults.pcm.card 0
```

Edit `RadioPlayer.py` and change `0` to `1` in the following lines:
```
sound_card_number = 0
```

## Locale

Before using the alarm, remember to set your time zone with `sudo raspi-config`.

## Get the url of a webradio

Go to the radio's webpage, start streaming it, and then find the streaming url in the network logging tab of your web browser, as explained [here](https://stackoverflow.com/questions/28314897/how-to-get-direct-streaming-url-from-this-flash-online-streaming-radio-station).

## Side issues

### Status led

To show the Raspberry status on a GPIO led, as explained [here](https://forums.raspberrypi.com/viewtopic.php?t=146455), edit `/boot/config.txt` and add:
```
dtoverlay=pi3-act-led,activelow=on,gpio=18
```
### Wifi dongle

Here is how to get a Realtek dongle to work on the Raspberry, as explained [here](https://forums.raspberrypi.com/viewtopic.php?t=285488):

```
sudo wget http://downloads.fars-robotics.net/wifi-drivers/install-wifi -O /usr/bin/install-wifi
sudo chmod +x /usr/bin/install-wifi
```
(Does not work any more with new kernel 5.10.63+.)

## To do

- Prepare a script for streaming
- Use button to switch off radio
- Switch on and off the amplifier
- Set the volume of alarms
- Add a recovery soundtrack in case of streaming failure
