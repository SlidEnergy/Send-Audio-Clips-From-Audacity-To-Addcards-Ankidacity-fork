# License AGPLv3
# copyright (c): 2015 Tiago Barroso
#                2019 ijgnd

import os

from PyQt5.QtGui import *

from aqt import addons, mw
from aqt.utils import showInfo

config = mw.addonManager.getConfig(__name__)
addon_dir_path = os.path.join(os.path.dirname(__file__))
ANKIDACITY_NY_FNAME = "ankidacity.ny"
ny_file_path = os.path.join(addon_dir_path, ANKIDACITY_NY_FNAME)


file_contents = '''
;nyquist plug-in
;version 1
;type process
;name "AnkiDacity"
;info "Saves the selection in a place where Anki can get it and add it to a card"
(setf *addon-dir*
      "{0:s}/")
(setf *media-file-path*
      (strcat *addon-dir* "media-file/ANKIDACITY-FILE"))
(setf *ready-file-path*
      (strcat *addon-dir* "ready/READY"))
(setf *max-length* 1000000000)
(s-save s *max-length* *media-file-path* :play NIL)
; Save a dummy sound file, just to tell anki we're ready
(s-save (pwl 0.1) *max-length* *ready-file-path* :play NIL)
s ; Returns the sound 
'''.format(addon_dir_path).replace("\\","/")


MSG = '''
<b>Audacity Integration addon</b>:<br/>
A file named <tt>{0:s}</tt> has been created
in the directory <br/><tt>{1:s}</tt><br/>
Please move or copy that file
to your <b>Audacity Plugins</b> directory. You can find
the correct directory in the Audacity documentation.
'''.format(ANKIDACITY_NY_FNAME, ny_file_path)

def audacity_integration_install():
    print(ny_file_path)

    f = open(ny_file_path, 'w')
    f.write(file_contents)
    f.close()

    showInfo(MSG)
