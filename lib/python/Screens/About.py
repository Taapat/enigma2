from Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from Tools.HardwareInfo import HardwareInfo
import os

from Tools.DreamboxHardware import getFPVersion

class About(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self["NetworkHeader"] = StaticText(_("Network:"))
		self["Network"] = StaticText(about.getNetworkInfo())
		self["EnigmaVersion"] = StaticText("Firmware: BlackHole " + about.getImageVersionString() + about.getSubVersionString())
		self["ImageVersion"] = StaticText("Build: " + about.getEnigmaVersionString())
		self["DriverVersion"] =  StaticText(_("DVB drivers: ") + about.getDriverDateString())
		self["KernelVersion"] =  StaticText(_("Kernel version: ") + about.getKernelVersionString())
		self["FPVersion"] = StaticText("Team Home: www.vuplus-community.net")
		self["CpuInfo"] =  StaticText(_("CPU: ") + self.getCPUInfoString())
		self["TunerHeader"] = StaticText(_("Detected NIMs:"))

		nims = nimmanager.nimList()
		if len(nims) <= 4 :
			for count in (0, 1, 2, 3):
				if count < len(nims):
					self["Tuner" + str(count)] = StaticText(nims[count])
				else:
					self["Tuner" + str(count)] = StaticText("")
		else:
			desc_list = []
			count = 0
			cur_idx = -1
			while count < len(nims):
				data = nims[count].split(":")
				idx = data[0].strip('Tuner').strip()
				desc = data[1].strip()
				if desc_list and desc_list[cur_idx]['desc'] == desc:
					desc_list[cur_idx]['end'] = idx
				else:
					desc_list.append({'desc' : desc, 'start' : idx, 'end' : idx})
					cur_idx += 1
				count += 1

			for count in (0, 1, 2, 3):
				if count < len(desc_list):
					if desc_list[count]['start'] == desc_list[count]['end']:
						text = "Tuner %s: %s" % (desc_list[count]['start'], desc_list[count]['desc'])
					else:
						text = "Tuner %s-%s: %s" % (desc_list[count]['start'], desc_list[count]['end'], desc_list[count]['desc'])
				else:
					text = ""

				self["Tuner" + str(count)] = StaticText(text)

		self["HDDHeader"] = StaticText(_("Detected HDD:"))
		hddlist = harddiskmanager.HDDList()
		hdd = hddlist and hddlist[0][1] or None
		if hdd is not None and hdd.model() != "":
			self["hddA"] = StaticText(_("%s\n(%s, %d MB free)") % (hdd.model(), hdd.capacity(),hdd.free()))
		else:
			self["hddA"] = StaticText(_("none"))

		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.close,
				"ok": self.close,
			})


	def getCPUInfoString(self):
		mhz = "MHz"
		cpu_count = 0
		cpu_speed = "n/a"
		if HardwareInfo().get_vu_device_name() == "duo4k":
			cpu_speed = "2.1"
			mhz = "GHz"
		elif HardwareInfo().get_vu_device_name() in ("solo4k", "ultimo4k", "zero4k", "duo4kse") :
			cpu_speed = "1.5"
			mhz = "GHz"
		elif HardwareInfo().get_vu_device_name() in ("uno4k", "uno4kse") :
			cpu_speed = "1.7"
			mhz = "GHz"
		try:
			for line in open("/proc/cpuinfo").readlines():
				line = [x.strip() for x in line.strip().split(":")]
				if line[0] == "model name":
					processor = line[1].split()[0]
				if line[0] == "system type":
					processor = line[1].split()[0]
				if line[0] == "cpu MHz":
					cpu_speed = "%1.0f" % float(line[1])
				if line[0] == "processor":
					cpu_count += 1
			return "%s %s %s %d cores" % (processor, cpu_speed, mhz, cpu_count)
		except:
			return _("undefined")



