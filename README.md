#MPD2MD

Push currently playing MPD track to a local or remote text file.

## Options

If no need to push via SCP, feel free to comment out self.push2webscp(). 

Only options that required to be set
    self.server = "Your SSH host"
    self.remotepath = "/path/to/file" # Where you want the generated file saved.

Note: When copying to remote server over ssh/scp, ensure you've set up ssh-copy-id to allow non-interactive ssh (ie: Key based auth, not password based)

## Use cases

Assign to a keyboard shortcut (xbindkeys?) to ensure you remember currently playing song. Especially suited to programmers with concentration spans easily broken.

Example key binding in your ~/.xbindkeysrc:
    "/path/to/mpd2md.py"
        Control + mod4 + s

## Python Requirements

* paramiko
* mpd

