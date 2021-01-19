# Copyright (c) 2014, SRI International
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ----------------------------------------------------------------------

"""
This module handles basic operations for receiving and sending messages via a
network socket to Pathway Tools. No major class is defined in this file, but
only toplevel functions and some simple classes for errors handling.
"""

import json, os, sys, socket, time
import pythoncyc.config

def recvAll(open_socket):
	"""
	Description
		Receive the entire message sent by Pathway Tools on an open socket. The message starts
		with a single character type, which is either 'A' or 'L'. The 'A' time is used
		without providing a length but can take longer to receive because it uses a
		timeout technique to read the entire message. The 'L' type assumes that the
		length of the message, in characters, is given on the next 10 characters as an
		integer. The message length is the number of characters after these 10
		characters.

	Parm
		open_socket, an open network socket.

	Return
		the message received on socket s as a string.
	"""
	if pythoncyc.config._debug:
		print('recvAll ...')

	# Get the type of message which is one character long.
	msg_type = open_socket.recv(1)

	if pythoncyc.config._debug:
		print("type ", msg_type)

	if msg_type == b'A':
		# The length of the message is not given, use time out approach.
		return recvTimeOut(open_socket)
	elif msg_type == b'L':
		# The next 10 characters give the length.
		lengthMsg = int(recvFixedLength(open_socket, 10))
		if pythoncyc.config._debug:
			print("lengthMsg {:d}".format(lengthMsg))
		return recvFixedLength(open_socket, lengthMsg)
	else:
		# Something is broken on the server side, so
		# use recv with a long timeout to try flushing
		# the sent message.
		return recvTimeOut(open_socket, timeOut=5)

def sendAll(open_socket, query):
	sent_len  = 0
	query_len = len(query)
	while sent_len < query_len:
		nb_chars = open_socket.send(query[sent_len:])
		if nb_chars == 0:
			raise PythonCycError("Connection to Pathway Tools broke while sending query {:s}.".format(query))
		sent_len = sent_len + nb_chars

def recvFixedLength(open_socket, lengthMsg):
	"""
	Description
		Receive a fixed length message on an open socket.

	Parm
		lengthMsg, an integer, which is the length in characters of the message to receive.

	Return
		the message received as a string.
	"""
	pieces = []
	nbBytesRecv = 0
	while nbBytesRecv < lengthMsg:
		piece = open_socket.recv(min(lengthMsg - nbBytesRecv, 4096))
		if piece == '':
			# Give up now because nothing was received.
			return ''.join(pieces)
		pieces.append(piece.decode())
		nbBytesRecv = nbBytesRecv + len(piece)
	# print 'Fixed receive: ',  ''.join(pieces)
	return ''.join(pieces)

def recvTimeOut(open_socket, timeOut=2):
	"""
	Description
		Receive a message of unknown length on socket. While receiving a message, if no
		more characters are sent on socket after timeOut seconds, it is assumed that the
		message has ended. Therefore, it will always, whatever the lenght of the
		message, take at least timeOut seconds to execute this method. If no character
		is received after 60 seconds, this method returns with an empty message.

	Parms
		open_socket
			an open network socket.
		timeOut
			number of seconds before timing out between fragments of the received message.

	Return
		The received message, as a string, on socket.
	"""
	# Keep each received packet in an array.
	pieces = []

	# Keep track of time between recvs.
	begin = time.time()

	while 1:
		# If we started to get data and the timeOut occurs,
		# we assume that Pathway Tools sent everything.
		if pieces and time.time() - begin > timeOut:
			break
		elif time.time() - begin > 60:
			break
		# Try to receive some text.
		try:
			data = open_socket.recv(4096)
			if data:
				print(data)
				pieces.append(data.decode())
				# Reset beginning time for next recv.
				begin = time.time()
			else:
				# Slow down in case timeOut is small.
				time.sleep(0.1)
		except socket.error:
			pass

	# Join all the pieces together.
	if pieces == []:
		return None
	else:
		return ''.join(pieces)

# Call a PTools function synchronously for any PGDB.
def sendQueryToPTools(query):
	"""
	Description
		Send a query to a running Pathway Tools application via a socket.

	Parm
		query, a string that the Python server in Pathway Tools can evaluate.

	Returns
		The result of the query, as a Python object, decoded by JSON.
	"""
	if pythoncyc.config._debug:
		print('Sending query ' + query)

	if pythoncyc.config._hostname == '':
	   raise PToolsError('The hostname to connect to a running Pathway Tools has not been set. Use function pythoncyc.config.set_hostname() to set the host name of your running Pathway Tools.')

	try:
		time.sleep(0.001)
		open_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Make socket non blocking.
		open_socket.setblocking(0)
		open_socket.settimeout(720)#open_socket.settimeout(360)  # The query may take a long time in some cases.
		open_socket.connect((pythoncyc.config._hostname, pythoncyc.config._hostport))
	except socket.error as msg:
		raise PToolsError('Failed to create a connection to a running Pathway Tools at ' + pythoncyc.config._hostname + ' on port ' + str(pythoncyc.config._hostport) + '. Make sure Pathway Tools is running with option -python. Error code: ' + str(msg[0]) + ', error message: ' + msg[1])

	# Send, receive and close socket.
	sendAll(open_socket, query.encode())

	if pythoncyc.config._debug:
		print('Sent ' + query + ' to Pathway Tools.')

	response = recvAll(open_socket)
	if pythoncyc.config._debug and len(response) < 4000:
		print('JSON Received: {:s}'.format(response))
	msg = json.loads(response)
	open_socket.close()

	if isinstance(msg, str) and msg.startswith(':error'):
		raise PToolsError('An internal error occurred in the running Pathway Tools application: {:s}'.format(msg))
	else:
		# Return some result.
		return msg

class PythonCycError(Exception):
	"""
	Error generated by one of the module of PythonCyc due to an incorrect
	use of its methods or functions.
	"""
	pass

class PToolsError(Exception):
	"""
	Error generated when Pathway Tools send an error due to its own Lisp execution.
	"""
	pass

