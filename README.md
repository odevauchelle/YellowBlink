# YellowBlink

A tiny server based on [Bottle](https://bottlepy.org/docs/dev/) to set up a webradio alarm clock on a Raspberry Pi. This project was inspired from [Piclodio](https://github.com/Sispheor/piclodio3), but it is written from scratch.

## Usage

Run `LungFish.py` and access [`http://localhost:8080/`](http://localhost:8080/) with a web browser.

## Dependencies

Tested on Debian and Raspberry Pi OS (Bullseye).

```
pip install bottle
```
```
apt-get install mplayer python-crontab
```

## Get the url of a webradio

Go to the radio's webpage, play it, and then find the streaming url in the network logging tab of your web browser, as explained [here](https://stackoverflow.com/questions/28314897/how-to-get-direct-streaming-url-from-this-flash-online-streaming-radio-station).

## Side issues

### Status led

To show the Raspberry status on a GPIO led, as explained [here](https://forums.raspberrypi.com/viewtopic.php?t=146455), edit `/boot/config.txt` and add:
```
dtoverlay=pi3-act-led,activelow=on,gpio=16
```
### Wifi dongle

Here is how to get a Realtek dongle to work on the Raspberry, as explained [here](https://forums.raspberrypi.com/viewtopic.php?t=285488):

```
sudo wget http://downloads.fars-robotics.net/wifi-drivers/install-wifi -O /usr/bin/install-wifi
sudo chmod +x /usr/bin/install-wifi
```
