#!/usr/bin/env python2
from mpd import MPDClient
import paramiko
import os
from datetime import datetime

class MPD2Web:
	def __init__(self):
		self.client = MPDClient()
		self.client.timeout = 10
		self.client.idletimeout = None
		self.client.connect("localhost",6600)
		self.filename = 'outfile.txt'
		self.server = 'localhost' # SSH host, requires password-less/key based auth
		self.remotepath = '/tmp/likedsongs.md' # Change this to location on remote server.

	def current_song(self):
		current_song = self.client.currentsong()
		self.client.close()
		self.client.disconnect()
		title = current_song['title']
		name = current_song['name']
		return "%s" % (title)

	# Check to make sure we haven't accidentally liked the same song twice
	# (This is only checking the last entry)
	def check_last_entry(self,current):
	    with open(self.filename, 'r') as f:
	        f.seek(-2,2)
	        while f.read(1) != b"\n":
	            f.seek(-2,1)
	        last = f.readline()[:-1]
	        f.close()
		if(current == last):
			return False
		else:
			return True

	def push2md(self):
		now = datetime.now()
		time = str(datetime.strftime(now,"%Y-%m-%d"))
		currentsong = "    "+time+" "+self.current_song()
		if(self.check_last_entry(currentsong)):
			with open(self.filename, 'a') as out:
				out.write(currentsong+"\n")
			out.close()
			print("{} added.").format(currentsong)
		else:
			print("Song already added to last entry")

	def push2webscp(self):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.load_system_host_keys()
		ssh.connect(self.server, username='james')
		sftp = ssh.open_sftp()
		sftp.put(self.filename, self.remotepath)
		sftp.close()
		ssh.close()

	def run(self):
		self.push2md()
		self.push2webscp()

if __name__ == '__main__':
	MPD2Web().run()
