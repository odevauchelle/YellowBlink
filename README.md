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
apt-get install mpg123 python3-alsaaudio python3-crontab python3-pip
```


```
pip3 install bottle RPi.GPIO
```

To use DAB+ radio:

```
apt-get install welle.io
```

## Sound card

Edit `/usr/share/alsa/alsa.conf` and change `0` to `1` in the following lines:
```
defaults.ctl.card 0
defaults.pcm.card 0
```

For a HifiBerry DAC+ soundcard, the install procedure is [here](https://www.hifiberry.com/docs/archive/hifiberry-software-configuration/).

## Locale

Before using the alarm, remember to set your time zone with `sudo raspi-config`.

## Get the url of a webradio

Go to the radio's webpage, start streaming it, and then find the streaming url in the network logging tab of your web browser, as explained [here](https://stackoverflow.com/questions/28314897/how-to-get-direct-streaming-url-from-this-flash-online-streaming-radio-station).

## Recovery file

A recovery audio file with a name ending in `.mp3` should be put in the `recovery_file` directory.

## GPIO pins

For the alarm clock:

| Use | GPIO |
|--|--|
| Status led | 18 |
| Amp switch | 17 |
| Button | 24 |

For the DAB+ radio player:

| Use | GPIO |
|--|--|
| Status led | 17 |
| Rotary encoder | 10 & 9 |
| Rotary push | 11 |
| Mode switch | 23 |

## Status led

To show the Raspberry status on a GPIO led, as explained [here](https://forums.raspberrypi.com/viewtopic.php?t=146455), edit `/boot/config.txt` and add:
```
dtoverlay=pi3-act-led,activelow=on,gpio=18
```
