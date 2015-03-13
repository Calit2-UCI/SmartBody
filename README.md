# SmartBody - RIVA Project

The **RIVA (Realistic Interactive Virtual Agent)** Project is being developed at the University of California, Irvine (Calit2). The goal of this system is to create a virtual assistant that provides feedback to patients undergoing physical rehabilitation with the [Music Glove](https://www.flintrehabilitation.com/).

The project utilizes USC's [Smartbody](http://smartbody.ict.usc.edu/) system, and is controlled using the Python scripting language through the **VirtualAssistant.py** script. This script relies on output from our [Music Glove Script](https://github.com/Calit2-UCI/MusicGlove).

##### In Progress...
- [ ] Improve character lighting
- [ ] Include 3D objects for the environment
- [ ] Concatenate audio files
- [ ] Differentiate between positive and negative feedback
- [ ] Improve character behavior (gestures, expressions)

## Contents
- [How to Run](#how-to-run)
- [Using with MusicGlove](#using-with-musicglove)
- [Gazing Coordinates](#gazing-coordinates)
- [Facial Expression BMLs](#facial-expression-bmls)

## How to Run
1. RUN the Music Glove Script
2. RUN sbgui.exe
3. SELECT File > Run Script > VirtualAssistant.py
4. RUN MusicGlove

## Using with MusicGlove

### Log File Format
* `Iteration:13;Expression:1;TTS:OVERALL_SUMMARY_2`

### Reading MusicGlove script output
* VirtualAssistant.py reads from the MusicGlove log file. If the file has been updated, RIVA will execute the appropriate actions.

## Gazing Coordinates
* z-coordinate: 1.0 onscreen, 1.5 offscreen
* Gaze Forward: `(0.03, 1.58, z)`
* Gaze Left: `(-4, 1.58, z)`
* Gaze Right: `(4, 1.58, z)`

## Facial Expression BMLs
* Happy:
  ```
	bml.execBML('ChrRachel', '<face type="facs" au="6" amount="1"/><face type="facs" au="12" amount="1"/>')
	```
* Sad:
  ```
	bml.execBML('ChrRachel', '<face type="facs" au="1_left" amount="1"/><face type="facs" au="1_right" amount="1"/> +
      <face type="facs" au="4_left" amount="1"/><face type="facs" au="4_right" amount="1"/> +
      <face type="facs" au="6" amount="0.58"/>')
	```
