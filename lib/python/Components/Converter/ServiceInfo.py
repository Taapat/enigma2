from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached

WIDESCREEN = [1, 3, 4, 7, 8, 0xB, 0xC, 0xF, 0x10]

class ServiceInfo(Converter, object):
	HAS_TELETEXT = 0
	IS_MULTICHANNEL = 1
	IS_CRYPTED = 2
	AUDIO_STEREO = 3
	IS_WIDESCREEN = 4
	IS_NOT_WIDESCREEN = 5
	SUBSERVICES_AVAILABLE = 6
	XRES = 7
	YRES = 8
	APID = 9
	VPID = 10
	PCRPID = 11
	PMTPID = 12
	TXTPID = 13
	TSID = 14
	ONID = 15
	SID = 16
	FRAMERATE = 17
	TRANSFERBPS = 18
	HAS_HBBTV = 19
	SUBTITLES_AVAILABLE = 20
	IS_STREAM = 21
	IS_SD = 22
	IS_HD = 23
	IS_1080 = 24
	IS_720 = 25
	IS_576 = 26
	IS_480 = 27
	IS_4K = 28
	IS_IPSTREAM = 29

	def __init__(self, type):
		Converter.__init__(self, type)
		self.type, self.interesting_events = {
			"HasTelext": (self.HAS_TELETEXT, (iPlayableService.evUpdatedInfo,)),
			"IsMultichannel": (self.IS_MULTICHANNEL, (iPlayableService.evUpdatedInfo,)),
			"IsCrypted": (self.IS_CRYPTED, (iPlayableService.evUpdatedInfo,)),
			"IsWidescreen": (self.IS_WIDESCREEN, (iPlayableService.evVideoSizeChanged,)),
			"IsNotWidescreen": (self.IS_NOT_WIDESCREEN, (iPlayableService.evVideoSizeChanged,)),
			"SubservicesAvailable": (self.SUBSERVICES_AVAILABLE, (iPlayableService.evUpdatedEventInfo,)),
			"VideoWidth": (self.XRES, (iPlayableService.evVideoSizeChanged,)),
			"VideoHeight": (self.YRES, (iPlayableService.evVideoSizeChanged,)),
			"AudioPid": (self.APID, (iPlayableService.evUpdatedInfo,)),
			"VideoPid": (self.VPID, (iPlayableService.evUpdatedInfo,)),
			"PcrPid": (self.PCRPID, (iPlayableService.evUpdatedInfo,)),
			"PmtPid": (self.PMTPID, (iPlayableService.evUpdatedInfo,)),
			"TxtPid": (self.TXTPID, (iPlayableService.evUpdatedInfo,)),
			"TsId": (self.TSID, (iPlayableService.evUpdatedInfo,)),
			"OnId": (self.ONID, (iPlayableService.evUpdatedInfo,)),
			"Sid": (self.SID, (iPlayableService.evUpdatedInfo,)),
			"Framerate": (self.FRAMERATE, (iPlayableService.evVideoSizeChanged,iPlayableService.evUpdatedInfo,)),
			"TransferBPS": (self.TRANSFERBPS, (iPlayableService.evUpdatedInfo,)),
			"HasHBBTV": (self.HAS_HBBTV, (iPlayableService.evUpdatedInfo,iPlayableService.evHBBTVInfo,)),
			"SubtitlesAvailable": (self.SUBTITLES_AVAILABLE, (iPlayableService.evUpdatedInfo,)),
			"IsStream": (self.IS_STREAM, (iPlayableService.evUpdatedInfo,)),
			"IsSD": (self.IS_SD, (iPlayableService.evVideoSizeChanged,)),
			"IsHD": (self.IS_HD, (iPlayableService.evVideoSizeChanged,)),
			"Is1080": (self.IS_1080, (iPlayableService.evVideoSizeChanged,)),
			"Is720": (self.IS_720, (iPlayableService.evVideoSizeChanged,)),
			"Is576": (self.IS_576, (iPlayableService.evVideoSizeChanged,)),
			"Is480": (self.IS_480, (iPlayableService.evVideoSizeChanged,)),
			"Is4K": (self.IS_4K, (iPlayableService.evVideoSizeChanged,)),
			"IsIPStream": (self.IS_IPSTREAM, (iPlayableService.evUpdatedInfo,)),
		}[type]

	def getServiceInfoString(self, info, what, convert = lambda x: "%d" % x):
		v = info.getInfo(what)
		if v == -1:
			return "N/A"
		if v == -2:
			return info.getInfoString(what)
		return convert(v)

	@cached
	def getBoolean(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return False
		video_width = info.getInfo(iServiceInformation.sVideoWidth)
		video_height = info.getInfo(iServiceInformation.sVideoHeight)
		video_aspect = info.getInfo(iServiceInformation.sAspect)
		if self.type == self.HAS_TELETEXT:
			tpid = info.getInfo(iServiceInformation.sTXTPID)
			return tpid != -1
		elif self.type in (self.IS_MULTICHANNEL, self.AUDIO_STEREO):
			# FIXME. but currently iAudioTrackInfo doesn't provide more information.
			audio = service.audioTracks()
			if audio:
				n = audio.getNumberOfTracks()
				idx = 0
				while idx < n:
					i = audio.getTrackInfo(idx)
					description = i.getDescription()
					if "AC3" in description or "AC3" in description or "AC-3" in description or "AC3+" in description or "AAC" in description  or "AAC-HE" in description or "DTS" in description or "Dolby Digital" in description:
						if self.type == self.IS_MULTICHANNEL:
							return True
						elif self.type == self.AUDIO_STEREO:
							return False
					idx += 1
				if self.type == self.IS_MULTICHANNEL:
					return False
				elif self.type == self.AUDIO_STEREO:
					return True
			return False
		elif self.type == self.SUBTITLES_AVAILABLE:
			try:
				subtitle = service and service.subtitle()
				subtitlelist = subtitle and subtitle.getSubtitleList()
				if subtitlelist:
					return len(subtitlelist) > 0
				return False
			except:
				try:
					subtitle = service and service.subtitleTracks()
					return subtitle and subtitle.getNumberOfSubtitleTracks() > 0
				except:
					return False
		elif self.type == self.IS_CRYPTED:
			return info.getInfo(iServiceInformation.sIsCrypted) == 1
		elif self.type == self.IS_WIDESCREEN:
			return video_aspect in WIDESCREEN
		elif self.type == self.IS_NOT_WIDESCREEN:
			return video_aspect not in WIDESCREEN
		elif self.type == self.SUBSERVICES_AVAILABLE:
			subservices = service.subServices()
			return subservices and subservices.getNumberOfSubservices() > 0
		elif self.type == self.HAS_HBBTV:
			return info.getInfoString(iServiceInformation.sHBBTVUrl) != ""
		elif self.type == self.IS_STREAM:
			return service.streamed() is not None
		elif self.type == self.IS_SD:
			return video_width > 1 and video_width <= 1024 and video_height > 1 and video_height <= 578
		elif self.type == self.IS_HD:
				return video_width > 1025 and video_width <= 1920 and video_height >= 481 and video_height < 1440 or video_width == 960 and video_height == 720
		elif self.type == self.IS_1080:
			return video_width >= 1366 and video_width <= 1980 and video_height >= 769 and video_height <= 1440
		elif self.type == self.IS_720:
			return video_width >= 1025 and video_width <= 1366 and video_height >= 481 and video_height <= 768 or video_width == 960 and video_height == 720
		elif self.type == self.IS_576:
			return video_width > 1 and video_width <= 1024 and video_height > 481 and video_height <= 578
		elif self.type == self.IS_480:
			return video_width > 1 and video_width <= 1024 and video_height > 1 and video_height <= 480
		elif self.type == self.IS_4K:
				return video_height >= 1460
		elif self.type == self.IS_IPSTREAM:
			return service.streamed() is not None
		return False


	boolean = property(getBoolean)

	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return ""
		if self.type == self.XRES:
			return self.getServiceInfoString(info, iServiceInformation.sVideoWidth)
		elif self.type == self.YRES:
			return self.getServiceInfoString(info, iServiceInformation.sVideoHeight)
		elif self.type == self.APID:
			return self.getServiceInfoString(info, iServiceInformation.sAudioPID)
		elif self.type == self.VPID:
			return self.getServiceInfoString(info, iServiceInformation.sVideoPID)
		elif self.type == self.PCRPID:
			return self.getServiceInfoString(info, iServiceInformation.sPCRPID)
		elif self.type == self.PMTPID:
			return self.getServiceInfoString(info, iServiceInformation.sPMTPID)
		elif self.type == self.TXTPID:
			return self.getServiceInfoString(info, iServiceInformation.sTXTPID)
		elif self.type == self.TSID:
			return self.getServiceInfoString(info, iServiceInformation.sTSID)
		elif self.type == self.ONID:
			return self.getServiceInfoString(info, iServiceInformation.sONID)
		elif self.type == self.SID:
			return self.getServiceInfoString(info, iServiceInformation.sSID)
		elif self.type == self.FRAMERATE:
			return self.getServiceInfoString(info, iServiceInformation.sFrameRate, lambda x: "%d fps" % ((x+500)/1000))
		elif self.type == self.TRANSFERBPS:
			return self.getServiceInfoString(info, iServiceInformation.sTransferBPS, lambda x: "%d kB/s" % (x/1024))
		return ""

	text = property(getText)

	@cached
	def getValue(self):
		service = self.source.service
		info = service and service.info()
		if not info:
			return -1
		if self.type == self.XRES:
			return info.getInfo(iServiceInformation.sVideoWidth)
		if self.type == self.YRES:
			return info.getInfo(iServiceInformation.sVideoHeight)
		if self.type == self.FRAMERATE:
			return info.getInfo(iServiceInformation.sFrameRate)

		return -1

	value = property(getValue)

	def changed(self, what):
		if what[0] != self.CHANGED_SPECIFIC or what[1] in self.interesting_events:
			Converter.changed(self, what)
