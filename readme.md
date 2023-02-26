![](https://i.ibb.co/x6T57dt/IMG-20230222-071157.jpg)
A screenshot of the StyloDuino Virtual Midi Controller.

![](https://i.ibb.co/g42G5g3/IMG-20230222-072120.jpg)
A screenshot of StyloDuino's PCB.

# What?
StyloDuino is an open-source, arduino-based alternative project for a [Stylohphone](https://en.wikipedia.org/wiki/Stylophone).
# Why?
The original Stylophone were designed to only be played, and can only provide one sound. I know some are actually admiring and purposefully looking for that *authentic* sound, here are some things StyloDuino can do while the other can't:

- **Customizability**
	StyloDuino can be customized on every aspect of the product, thus including:
	
	- **The Sound**
		Whether to be played on its own or use it as a midi controller, the sound can be extensively customized. You could write your own Arduino-based synthesizer or use the open source one like [Mozzi](https://sensorium.github.io/Mozzi/). The arduino's speed is literally your limit.
		
	- **The Hardware**
			Want your StyloDuino to have an amplifier? No problem! You can modify the PCB all you like, all by yourself. You can use common software available such as Altium, AutoCAD, Eagle, EasyEDA, etc. You can then export it as Gerber file and upload it to a pcb manufacturing company such as [JLCPCB](https://jlcpcb.com/) or [PCBWay](https://www.pcbway.com/). Or export it as printing mask so you could print it yourself.

- **MIDI Support**
		MIDI is supported via StyloDuino-VMC (Virtual Midi Controller) which you could download on the release page. [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) is required for the controller to work. After installing loopMIDI, create a virtual midi with the name ``styloduino`` and then have fun!

- **You can build it yourself**
	That's where the fun come begin.

