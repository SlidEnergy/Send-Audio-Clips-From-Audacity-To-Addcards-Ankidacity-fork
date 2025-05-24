# AnkiDacity

## Overview

Anki is frequently used for language learning. Audio in cards can be very useful and fun, but cutting little audio clips and adding them to Anki is time consuming and boring. You have to:

1. Open the file in an audio editor (like [Audacity](https://web.archive.org/web/20190511115051/http://audacityteam.org/)).
2. Select the clip.
3. Save as a new file.
4. Use Anki’s dialog to add the clip to your note.
5. Repeat the from #2 to add more clips from the same audio file

This addon makes it much easier to add sound clips from Audacity.

## Installation

The installation of this addon requires moving some files around.

1. Install the addon
2. Restart Anki
3. Open Anki’s folder
4. Inside this folder, you will find a file named `AnkiDacity.ny`. This is an [Audacity plugin](https://web.archive.org/web/20190511115051/http://wiki.audacityteam.org/wiki/Download_Nyquist_Plug-ins), written in the nyquist programming language.
5. Place this file in your audacity plugins directory. This should in the directory where Audacity resides:
    - `C:\Program Files` or `C:\Program Files (x86)` on Windows.
    - the `Applications` folder on OS X.
    - `usr/share/Audacity` or `~/.audacity-files/plug-ins` (you can create it if it doesn’t exist)
6. Open Audacity
7. Check that the _AnkiDacity_ plugin is accessible from the _Effects_ menu (you might have to click _Plugins 1-15_ at the botom of the panel)
8. If it’s there, than everything should be ready to go.

## Usage

1. Open Anki’s _Add Note_ window.
2. Open the audio file in Audacity.
3. Go back to the _Add Note_ window and place the cursor where you want to insert the audio.
4. Go back to Audacity and select the clip you want to extract to Anki.
5. Open the _Effects_ menu and select _AnkiDacity_.
6. A new audio file containing the selection should be added to your note.
7. Add the note and repeat.

The great advantage of this addon is that you don’t need to save an intermediary audio file and add it using Anki’s dialog, which is time consuming, especially if you are going to add lots of audio clips to your notes.

Note that you can use Audacity’s `Ctrl + r` shortcut to repeat the most recently used plugin. This can save you some time if you’re adding more than one audio clip from the file.

## Issues

The addon work very well generally, but rarely Anki might fail to detect that a new audio file has been generated. **Techincal Explanation:** The Nyquist programming language, in which the Audacity part of the addon is written, is very limited. By design, Audacity can’t connect to external programs using TCP connections and nyquist doesn’t support launching external programs. There are ways for Audacity to communicate with external programs, but they seem to be linux specific and not portable. This leaves us with suboptimal ways to communicate between Audacity and Anki. The way the addon works now is by writing the audio file into a folder that Anki is always watching. Whenever a file is written to thar folder, Anki adds it to the current cursor position. Unfortunately, this doesn’t work as well as a TCP connection, and sometimes the addon fails to recognize that a file has been created.

At the same time, the installation process is still kind of rough, but since it is something the user only has to do once, I don’t think it’s worth it to automate it further.

## License

This addon is available under the BSD license
