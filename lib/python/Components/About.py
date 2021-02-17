from Tools.Directories import resolveFilename, SCOPE_SYSETC
from enigma import getEnigmaVersionString
from os import popen
from boxbranding import getImageVersion, getImageBuild, getDriverDate

class About:
	def __init__(self):
		pass

	def getImageVersionString(self):
		return getImageVersion()

	def getSubVersionString(self):
		if len( getImageBuild()) < 1:
			return ""
		else:
			return "." + getImageBuild()

	def getEnigmaVersionString(self):
		return getEnigmaVersionString()

	def getDriverDateString(self):
		return getDriverDate()

	def getKernelVersionString(self):
		try:
			return open("/proc/version","r").read().split(' ', 4)[2].split('-',2)[0]
		except:
			return _("unknown")

	def getIfaces(self):
		import socket, fcntl, struct, array, sys
		SIOCGIFCONF = 0x8912 # sockios.h
		is_64bits = sys.maxsize > 2**32
		struct_size = 40 if is_64bits else 32
		max_possible = 8 # initial value
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		while True:
			# ifconf structure:
			# struct ifconf {
			#		int			ifc_len; /* size of buffer */
			# 		union {
			# 			char 		*ifc_buf; /* buffer address */
			#			struct ifreq	*ifc_req; /* array of structures */
			# 		};
			# 	};
			#
			# struct ifreq:
			# #define IFNAMSIZ	16
			# struct ifreq {
			# 	char ifr_name[IFNAMSIZ]; /* Interface name */
			# 	union {
			# 		struct sockaddr ifr_addr;
			# 		.....
			# 	};
			# };

			# Initialize ifc_buf
			bytes = max_possible * struct_size
			names = array.array('B')
			for i in range(0, bytes):
				names.append(0)

			input_buffer = struct.pack( 'iL', bytes, names.buffer_info()[0] )
			output_buffer = fcntl.ioctl( sock.fileno(), SIOCGIFCONF, input_buffer )
			output_size = struct.unpack('iL', output_buffer)[0]

			if output_size == bytes:
				max_possible *= 2
			else:
				break

		namestr = names.tostring()
		ifaces = []
		for i in range(0, output_size, struct_size):
			iface_name = namestr[i:i+16].split('\0', 1)[0]
			iface_addr = socket.inet_ntoa(namestr[i+20:i+24])
			if iface_name != 'lo':
				ifaces.append((iface_name, iface_addr))

		return ifaces

	def getNetworkInfo(self):
		data = ""
		for x in self.getIfaces():
			data += "%s : %s\n" % (x[0], x[1])
		return data or "\tnot connected"

about = About()
