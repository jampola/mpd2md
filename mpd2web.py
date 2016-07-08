#!/usr/bin/python
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
		self.filename = 'out.txt'
		self.server = 'jamesbos.com'
		# self.remotepath = '/var/www/somehtml/staticpages/likedtunes.md'
		self.remotepath = '/home/james/likedtunes.md'

	# Call this to test if mpd is playing nice
	def mpd_version(self):
		return self.client.mpd_version

	def current_song(self):
		current_song = self.client.currentsong()
		self.client.close()
		self.client.disconnect()
		title = current_song['title']
		name = current_song['name']
		return "%s" % (title)

	def push2md(self):
		now = datetime.now()
		time = str(datetime.strftime(now,"%Y-%m-%d"))
		currentsong = self.current_song()
		outfile = open(self.filename,'a')
		outfile.write("    "+time+" "+currentsong+"\n")
		outfile.close()

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
