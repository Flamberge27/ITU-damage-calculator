"""
I dunno, maybe this should be a .json or something?

Whatever lol
#"""

from itu_classes import *
import math

def getHekaton(level = 1):

	# AT modification from primordial level
	at_mod = max(0, level - 3)
	if level == 0:
		at_mod = -1
		level = 1		# quick kludge; only difference between L1 and L2 is the AT. This makes the later math neater.
	# max(0) takes care of 0-2, (2/3)L + 1 gives us the 1-2-2-3-4-4-5 behavior we want, just needs to be modulated by the -2
	escalations = max(0, round((level - 2) * 2 / 3 + 1))
	# if we didn't do the kludge, this would give us 6 evasion at level 0
	eva = 6 + max(0, math.floor((level + 1) / 2))

	"""
	scourgeFail, scourgeWound = -1, 1	# start here by default
	if level >= 6:
		scourgeFail, scourgeWound = -1, 1	# this is where you would change these values, but scourge isn't actually that scary

	#"""

	BPs = [
		BPCard("One of a Hundred", AT=2, lvl = 1),
		BPCard("The Runt", AT=2, lvl = 1),
		BPCard("Right Mighty Fist", AT=3, lvl = 1),
		BPCard("Left Might Fist", AT=3, lvl = 1),
		BPCard("Right Shield Fist", AT=4, lvl = 1),
		BPCard("Left Shield Fist", goodness={'C': 2}, AT=4, lvl = 1),			# crit bonus attack + rare resources

		BPCard("Hand-Feet", AT=4, lvl = 2),
		BPCard("Exposed Back Arms", goodness={'C': 2}, AT=4, lvl = 2),			# additional single wound on crit = twice as good
		BPCard("Shoulderhands", AT=5, lvl = 2),
		BPCard("Knuckle Teeth", goodness={'C': 2}, AT=5, lvl = 2),				# crit bonus attack
		BPCard("Muscular Biceps Thighs", AT=5, lvl = 2),
		BPCard("Calcified Maze Places", goodness={'W': 0, 'C': 2}, AT=6, lvl = 2),		# crit loot, might rather fail to keep it possible

		BPCard("Hand-Head", At=5, lvl=3),
		BPCard("Spinal Finger Column", At=5, lvl=3),
		BPCard("Drum-Heart", At=6, lvl=3),										# debatably could be in 3 territory
		BPCard("One In a Hundred", goodness={'C': 3}, At=6, lvl=3),				# BP3 with crit for +1 wound
		BPCard("Humanity", At=7, lvl=3),										# could be a 3
		BPCard("Corruption's Root", goodness={'C': 3}, At=8, lvl=3)				# deathblow
	]
	for BP in BPs:
		BP.AT_base += at_mod

	return BPs, escalations, eva

class Primordial:
	def __init__(self, name, lvl = 1):
		self.name = name
		self.level = lvl

		if self.name == 'Hekaton':
			self.BPs, escalations, self.eva = getHekaton(lvl)
		# if self.name is [] and so on...

		self.deckCount = {
			'BP1': max(0, 6 - escalations),
			'BP2': min(escalations, 12 - escalations),
			'BP3': max(0, escalations - 6)
		}

		self.BPs_By_Name = dict([(card.name, card) for card in self.BPs])
		self.BPs_By_Status = dict([(card.name, 0) for card in self.BPs])		# status: 0 (possibly in deck), 

	def getBPChances(self, level):

		options = []

		for BPName, status in self.BPs_By_Status.items():

			# need status == 0 (unaccounted for) and correct level
			if status == 0 and BPCard.BPlevel == level:
				options.append(self.BPs_By_Name(BPName))