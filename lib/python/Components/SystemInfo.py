from enigma import eDVBResourceManager, eDVBCIInterfaces
from Tools.Directories import fileExists, fileCheck
from Tools.HardwareInfo import HardwareInfo

SystemInfo = { }

#FIXMEE...
def getNumVideoDecoders():
	idx = 0
	while fileExists("/dev/dvb/adapter0/video%d"%(idx), 'f'):
		idx += 1
	return idx

SystemInfo["NumVideoDecoders"] = getNumVideoDecoders()
SystemInfo["CanMeasureFrontendInputPower"] = eDVBResourceManager.getInstance().canMeasureFrontendInputPower()


def countFrontpanelLEDs():
	leds = 0
	if fileExists("/proc/stb/fp/led_set_pattern"):
		leds += 1

	while fileExists("/proc/stb/fp/led%d_pattern" % leds):
		leds += 1

	return leds

SystemInfo["NumFrontpanelLEDs"] = countFrontpanelLEDs()
SystemInfo["FrontpanelDisplay"] = fileExists("/dev/dbox/oled0") or fileExists("/dev/dbox/lcd0")
SystemInfo["FrontpanelDisplayGrayscale"] = fileExists("/dev/dbox/oled0")
SystemInfo["DeepstandbySupport"] = HardwareInfo().get_device_name() != "dm800"
SystemInfo["HdmiInSupport"] = HardwareInfo().get_vu_device_name() in ("ultimo4k", "uno4kse", "duo4k", "duo4kse")
SystemInfo["WOWLSupport"] = HardwareInfo().get_vu_device_name() in ("ultimo4k", "duo4k", "duo4kse")
SystemInfo["ScrambledPlayback"] = None
SystemInfo["FastChannelChange"] =  fileExists("/proc/stb/frontend/fbc/fcc")
SystemInfo["MiniTV"] = fileExists("/proc/stb/lcd/live_enable")
SystemInfo["DisableUsbRecord"] = HardwareInfo().get_vu_device_name() in ("meo", "eddi", "ev0")
SystemInfo["DefaultAniSpeed"] = HardwareInfo().get_vu_device_name() in ("uno4k", "uno4kse", "zero4k", "duo4k") and 25 or 20
SystemInfo["DefaultFullHDSkin"] = HardwareInfo().get_vu_device_name() in ("solo4k", "ultimo4k", "uno4k", "uno4kse", "zero4k", "duo4k", "duo4kse")
SystemInfo["PVRSupport"] = HardwareInfo().get_vu_device_name() not in ["meo", "eddi", "ev0"]
SystemInfo["CommonInterface"] = 1
SystemInfo["CommonInterfaceCIDelay"] = fileCheck("/proc/stb/tsmux/rmx_delay")
SystemInfo["CI1SupportsHighBitrates"] = None
SystemInfo["CI1RelevantPidsRoutingSupport"] = None

