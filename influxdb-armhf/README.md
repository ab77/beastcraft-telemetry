# InfluxDB (armhf)
* [influxdb_0.9.6_armhf.deb](https://s3.eu-central-1.amazonaws.com/beastcraft-telemetry/influxdb_0.9.6_armhf.deb)
* [influxdb_0.10.3-1_armhf.deb](https://s3.eu-central-1.amazonaws.com/beastcraft-telemetry/influxdb_0.10.3-1_armhf.deb)
* [influxdb_0.12.1-1_armhf.deb](https://s3.eu-central-1.amazonaws.com/beastcraft-telemetry/influxdb_0.12.1-1_armhf.deb)

### Build

```
# build
export VERSION=0.12.1
gvm use go1.4.3
gvm pkgset create influxdb
gvm pkgset use influxdb
cd ~/.gvm/pkgsets/go1.4.3/influxdb
export GOPATH=`pwd`
go get github.com/influxdata/influxdb || go get -u github.com/influxdata/influxdb
cd $GOPATH/src/github.com/influxdata/influxdb
./build.py --package --version=$VERSION --arch=armhf

# install
dpkg -i build/*.deb
```
