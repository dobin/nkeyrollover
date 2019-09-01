# nkeyrollover

* ASCII Beat Em Up 
* With MOBA controls

Follow the adventures of ASCIIMAN.



## History Lesson 

In the early days, computers were feed using paper punch cards, and produced results printed on paper. 

Then mainframes came around, where you could actually type on a keyboard, instead
of feeding it paper, and it showed the result on a primitive monitor, instead
of printing the result. Multi user support was developed, so that more than
one person can use the million dollar computer at once. Each at their own terminal. This was the short time where ASCII games were the only games available. 

Shortly after, 8-bit home computers were developed, and those with graphic
processing units quickly gained worldwide adoption (Commodore 64, Amiga). 
They could be used to play games, with graphics!

The timeframe for ASCII games was very short, and the art was lost forever. 

Or was it?

"Do not fold, spindle or mutilate. I am a student"

https://en.wikipedia.org/wiki/Text-based_game


## Mypy

```
python -m mypy nkeyrollover.py
```


## Tests 

* tests/animationplayer.py: play various animations
* unittest_test.py: test some stuff
* worldplayer.py: a simple world


### Unit tests

```
python -m unittest
```

## Telnet config 

Install: 
```
# apt install telnet telnetd
# cd /opt
# git clone https://github.com/dobin/nkeyrollover.git
# touch nkeyrollover/app.log
# chown game:game nkeyrollover/app.log
```

Configure:
```
# adduser game # password game
# chsh -s '/opt/nkeyrollover/nkeyrollover.py' game
```