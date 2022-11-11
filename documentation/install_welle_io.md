# Install Welle.io

[Welle.io](https://www.welle.io/) is a digital radio software (DAB+). It requires a receiver, such as a usbrtl-sdr (RTL2832U).

## Basic install

To install on Debian:

```console
apt-get install welle.io
```

To start the [client](https://github.com/AlbrechtL/welle.io#usage-of-welle-cli) :

```console
welle-cli -c 8C -w 8888
```

The channel, `8C`, corresponds to *Radio France* in Paris. The web interface can be accessed at http://localhost:8888.

To play a specific radio with the command line:

```console
mplayer http://localhost:8888/mp3/0xf204
```
The code `0xf204` corresponds to Fip radio in Paris.

## Latest version

To get the latest version of welle.io, follow the steps proposed [here](http://ale.cx/ALEX/category/tinkering/).

Dependencies:
```console
apt install libtool libusb-1.0-0-dev librtlsdr-dev rtl-sdr build-essential autoconf cmake pkg-config libfftw3-dev libmpg123-dev libfaad-dev libsoapysdr-dev
```

Install
```console
git clone https://github.com/AlbrechtL/welle.io
mkdir welle.io/build
cd welle.io/build/
cmake .. -DRTLSDR=1 -DSOAPYSDR=1 -DBUILD_WELLE_IO=OFF -DBUILD_WELLE_CLI=ON
make
make install
```
After this, `welle-cli` should be in `/usr/local/bin`.
