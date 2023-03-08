# WebThings Integration

Background:

- [WebThings Framework](https://webthings.io/framework/)

- [Python Library](https://github.com/WebThingsIO/webthing-python)


Install:

```
sudo pip3 install webthing
```

[Systemd](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)
service file in `/etc/systemd/system/`:

```
[Unit]
Description=WebThing Server
After=network.target

[Service]
ExecStart=python3 /PATH/TO/SCRIPT
User=pi

[Install]
WantedBy=multi-user.target
```
