# copyright (c): 2015 Tiago Barroso
#                2019- ijgnd

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.



from aqt.qt import *

import os
import time
import datetime
import shutil
import subprocess

from aqt import mw
from aqt.editor import Editor
from aqt.utils import tooltip

from . import install


def gc(arg, fail=False):
    try:
        out = mw.addonManager.getConfig(__name__).get(arg, fail)
    except:
        return fail
    else:
        return out



addon_dir_path = os.path.join(os.path.dirname(__file__))
READY_DROP_LOCATION = os.path.join(addon_dir_path, "ready")
MEDIA_DROP_LOCATION = os.path.join(addon_dir_path, "media-file")
ALREADY_INSTALLED_PATH = os.path.join(addon_dir_path, "already-installed.txt")


def already_installed():
    f = open(ALREADY_INSTALLED_PATH)
    state = f.readline()
    f.close()
    if state.startswith("True"):
        return True
    else:
        return False


def update_installed():
    f = open(ALREADY_INSTALLED_PATH, 'w')
    state = f.write("True")
    f.close()


def audacity_integration_setupWatcher(self):
    self.fswatcher = QFileSystemWatcher()
    self.fswatcher.addPath(READY_DROP_LOCATION)
Editor.audacity_integration_setupWatcher = audacity_integration_setupWatcher


def audacity_integration_listenToWatcher(self):
    self.fswatcher.directoryChanged.connect(self.audacity_integration_get_media)
Editor.audacity_integration_listenToWatcher = audacity_integration_listenToWatcher


def now():
    if gc("milliseconds_in_filename"):
        return datetime.datetime.now().strftime("%Y-%m-%d__%H_%M_%S__%f")
    else:
        return time.strftime('%Y-%m-%d__%H_%M_%S', time.localtime(time.time()))


def audacity_integration_get_media(self, path):
    tooltip(f"Watcher triggered! Path changed: {path}")
    media = os.listdir(MEDIA_DROP_LOCATION)
    ready = os.listdir(READY_DROP_LOCATION)
    # Sort the contents by alphabetical order to ensure deterministic
    # behaviour. If we have more than a file there, something's wrong,
    # but at least it will be deterministically wrong.
    media.sort()
    self.fswatcher.removePath(READY_DROP_LOCATION)
    ffmpeg = shutil.which("ffmpeg")
    #avoid undue burden on ankiweb and prevent import of wav etc.
    if not ffmpeg:
        tooltip('ffmpeg not found in PATH. Aborting ... Check the add-on documentation on ankiweb.')
        return
    for fname in media:
        asource = os.path.join(MEDIA_DROP_LOCATION,fname)
        ftype = gc("filetype", "mp3")
        ffmpeg_options = gc("ffmpeg_options", "").split()
        if not ftype.startswith("."):
            ftype = "." + ftype
        #avoid undue burden on ankiweb and prevent import of wav etc.
        if ftype not in [".opus",".mp3",".m4a"]:
            tooltip('Unknown extension detected. Falling back to ".mp3"')
            ftype = ".mp3"
        adest = now() + ftype
        output_path = os.path.join(MEDIA_DROP_LOCATION, adest)
        cmd_list = [ffmpeg, '-i', asource, *ffmpeg_options, output_path]
        #result = subprocess.call(cmd_list)
        process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        print("Return code:", process.returncode)
        print("STDOUT:", stdout.decode('utf-8'))
        print("STDERR:", stderr.decode('utf-8'))

        if os.path.isfile(output_path):
            print(f"File successfully created: {output_path}")
            filename = self.addMedia(output_path, canDelete=False)
            field = gc("field", "Audio")
            if hasattr(self, "note") and field in self.note:
                self.note[field] += f"[sound:{os.path.basename(output_path)}]"
                self.loadNote()
                tooltip(f"Audio added to the {field} field")
            else:
                tooltip(f"{field} field not found in the note")

    time.sleep(gc("clear_delay_in_seconds", 0.05))
    clear_dir(MEDIA_DROP_LOCATION)
    clear_dir(READY_DROP_LOCATION)
    self.fswatcher.addPath(READY_DROP_LOCATION)
Editor.audacity_integration_get_media = audacity_integration_get_media


def clear_dir(dir):
    contents = os.listdir(dir)
    for f in contents:
        while True:
            try:
                os.remove(os.path.join(dir, f))
                break
            except:
                time.sleep(0.01)


def new__init__(self, *args, **kwargs):
    old__init__(self, *args, **kwargs)
    clear_dir(READY_DROP_LOCATION)
    clear_dir(MEDIA_DROP_LOCATION)
    self.audacity_integration_setupWatcher()
    self.audacity_integration_listenToWatcher()
old__init__ = Editor.__init__
Editor.__init__ = new__init__



#empty folders are not unzipped, https://github.com/dae/anki/blob/master/aqt/addons.py#L231
for d in [READY_DROP_LOCATION, MEDIA_DROP_LOCATION]:
    if not os.path.isdir(d):
        os.makedirs(d)


if not already_installed():
    install.audacity_integration_install()
    update_installed()
