"""
Author: Mengxuan Xia <xiamx2004@gmail.com>
Last update: 2011/02/16
Description: This script can automatically print files located in 
dropbox printqueue. It is based on Kurt Granroth's original bash 
script http://www.labnol.org/software/print-files-on-linux/17841/. 
This script depends on pyinotify and pynotify. 

Copyright (c) 2011, Mengxuan Xia
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

	* Redistributions of source code must retain the above
	  copyright notice, this list of conditions and the 
	  following disclaimer.
	* Redistributions in binary form must reproduce the above
	  copyright notice, this list of conditions and the following
	  disclaimer in the documentation and/or other materials
	  provided with the distribution.
	* Neither the name of the Mengxuan Xia nor the names of
	  its contributors may be used to endorse or promote
	  products derived from this software without specific
	  prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,  
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY 
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
OF SUCH DAMAGE.
"""


import pyinotify
import subprocess
import os
import pynotify
import threading

# Print Queue Dir. As you can see, I have two PrintQueues Here
PrintQueue = ['/home/xiamx/Dropbox/PrintQueue/','/home/xiamx/Dropbox/Attachments/']


# The watch manager stores the watches and provides operations on watches
wm = pyinotify.WatchManager()

mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events

printoptions = " "

class EventHandler(pyinotify.ProcessEvent):
	def process_IN_CREATE(self, event):
		lpr (os.path.abspath( event.pathname))
		print "Printing: ", event.pathname
	def process_IN_DELETE(self, event):
		pass
		# print "Removing:", event.pathname
	
def lpr(pathname):
	#ignore file that doesn't exist
	if os.path.exists(pathname) == False:
		return
	#ignore file start with "."
	if os.path.basename(pathname)[0] == '.':
		return
	print(pathname)
	subprocess.Popen(["lpr","-r",pathname])
	n = pynotify.Notification("Printing",os.path.basename(pathname),'gtk-print')
	n.show()

def doGetNewFile():
	for p in PrintQueue:
		list = os.listdir(p)
		for file in list:
			lpr (os.path.join(p,file))
	
if __name__ == "__main__":
	t = threading.Timer(60.0,doGetNewFile)
	t.start()
	pynotify.init("Drop Print")
	handler = EventHandler()
	notifier = pyinotify.Notifier(wm, handler)
	# Internally, 'handler' is a callable object which on new events will be called like this: handler(new_event)
	for p in PrintQueue:
		wm.add_watch(p, mask, rec=True)
	notifier.loop()
