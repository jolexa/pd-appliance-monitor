pd-appliance-monitor
=======

Affix a RaspberryPi with 801s sensor attached, get paged via [PagerDuty](https://www.pagerduty.com/)
when your laundry is done.

### Why would I do this?
Basically, it is fun to play with RaspberryPi's.

Practically, I did this so I can reduce my mental energy remembering that my
laundry is in progress. This is at least, _somewhat practical_ since my laundry
is in the basement and I always forget about it.

### Run this for yourself
1. Connect the 801s sensor to the GPIO pins. I just jammed it in there because
the 5v, Ground, and Out pins lined up on the
[4, 6 & 8 pins](https://pinout.xyz/).
2. Configure a PagerDuty API Integration, obtain a service key
3. Run `PD_SERVICE_KEY=<key> python ./vibration.py` or some other variation of
the same command.

### End Result
![Screenshot](https://raw.githubusercontent.com/jolexa/pd-appliance-monitor/master/pi.jpg)
