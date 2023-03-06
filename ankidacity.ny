
;nyquist plug-in
;version 1
;type process
;name "AnkiDacity"
;info "Saves the selection in a place where Anki can get it and add it to a card"
(setf *addon-dir*
      "/home/lukas/.local/share/Anki2/addons21/1326170847/")
(setf *media-file-path*
      (strcat *addon-dir* "media-file/ANKIDACITY-FILE"))
(setf *ready-file-path*
      (strcat *addon-dir* "ready/READY"))
(setf *max-length* 1000000000)
(s-save s *max-length* *media-file-path* :play NIL)
; Save a dummy sound file, just to tell anki we're ready
(s-save (pwl 0.1) *max-length* *ready-file-path* :play NIL)
s ; Returns the sound 
