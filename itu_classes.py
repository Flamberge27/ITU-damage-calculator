import random

def addStrPiece(base_string, delim, quantity, text):
	ret_str = ""

	if quantity == 0:
		return ret_str

	if len(base_string) > 0:
		ret_str += delim

	ret_str += str(quantity) + text
	return ret_str

def formatDamageNums(pow = 0, pot = 0, dot = 0):
	ret_str = ""

	""" Tier List: Power symbols
	A: 3031, 3111 (not bold), 1331A (reversed, very light)
	B: 23AC, 0EC4
	C: 1D98, 0F3D, 2CD4, 2CD5
	Rectangles: 1C05, 1C2B, 1B04, 1046C, 18809, 1B045
	# """
	ret_str += addStrPiece(ret_str, '\t', pow, chr(int('3031', 16)))

	""" Other Potential symbols
	1F702, 25EC, 27C1, 9651
	# """
	ret_str += addStrPiece(ret_str, '\t', pot, chr(int('27C1', 16)))

	ret_str += addStrPiece(ret_str, '\t', dot, chr(int('2022', 16)))
	
	return ret_str

def formatDamageTuple(numTup):
	if len(numTup) == 2:
		return formatDamageNums(numTup[0], numTup[1], 0)
	return formatDamageNums(numTup[0], numTup[1], numTup[2])

class DieFace():
	def __init__(self, num, pow, pot, dot, compArr):
		self.number = num
		self.power = pow
		self.potential = pot
		self.dots = dot

		# comparison array to easily store/recall comparisons to other die faces
		# -1	this face is strictly worse
		#  0	this face is exactly equal to the other
		#  1	this face is situationally better/worse than the other
		#  2	this face is strictly better than the other
		self.comparisonArray = compArr

class DamageDie():
	def __init__(self, col):
		self.color = col


		if col == 'red':
			self.sides = [DieFace(0, 2, 0, 1, [ 0,  2,  2,  2,  2,  2]),
				 		  DieFace(1, 1, 1, 0, [-1,  0,  0,  2,  2,  2]),
						  DieFace(2, 1, 1, 0, [-1,  0,  0,  2,  2,  2]),
						  DieFace(3, 1, 0, 0, [-1, -1, -1,  0,  2,  2]),
						  DieFace(4, 0, 1, 0, [-1, -1, -1, -1,  0,  1]),
						  DieFace(5, 0, 0, 1, [-1, -1, -1, -1,  1,  0])]

		elif col == 'black':
			self.sides = [DieFace(0, 2, 2, 1, [ 0,  2,  2,  2,  2,  2]),
				 		  DieFace(1, 2, 1, 0, [-1,  0,  1,  2,  2,  2]),
						  DieFace(2, 2, 0, 1, [-1,  1,  0,  2,  2,  2]),
						  DieFace(3, 1, 1, 0, [-1, -1, -1,  0,  0,  2]),
						  DieFace(4, 1, 1, 0, [-1, -1, -1,  0,  0,  2]),
						  DieFace(5, 0, 1, 1, [-1, -1, -1, -1, -1,  0])]
		
		elif col == 'white':
			self.sides = [DieFace(0, 3, 2, 1, [ 0,  2,  2,  2,  2,  2]),
				 		  DieFace(1, 2, 3, 0, [-1,  0,  1,  2,  2,  2]),
						  DieFace(2, 2, 1, 1, [-1,  1,  0,  1,  2,  2]),
						  DieFace(3, 1, 3, 0, [-1, -1,  1,  0,  1,  1]),
						  DieFace(4, 1, 2, 1, [-1, -1, -1,  1,  0,  2]),
						  DieFace(5, 1, 1, 1, [-1, -1, -1,  1, -1,  0])]

		self.cur_side = -1

	def roll(self):
		self.cur_side = random.randint(0,5)

		return self.sides[self.cur_side]

class DiePool():
	def __init__(self, dice, dice_pool_dict, ignore_dots = False):
		if dice in dice_pool_dict:
			self.loadFromDict(dice_pool_dict, dice)
			return

		self.combo_mults = {} # 'combination multiplicities'
		self.total_mult = 0 # total multiplicity
		self.dice = dice

		# catch empty dice pool case
		if dice == (0, 0, 0):
			self.combo_mults[(0, 0, 0)] = 1
			self.total_mult = 1
			dice_pool_dict[(0, 0, 0)] = self
			return

		# set up combinations via lookback
		if dice[0] > 0:
			small_pool = DiePool((dice[0] - 1, dice[1], dice[2]), dice_pool_dict)
			new_die = DamageDie('red')

		elif dice[1] > 0:
			small_pool = DiePool((dice[0], dice[1] - 1, dice[2]), dice_pool_dict)
			new_die = DamageDie('black')

		elif dice[2] > 0:
			small_pool = DiePool((dice[0], dice[1], dice[2] - 1), dice_pool_dict)
			new_die = DamageDie('white')

		else:
			print("something went wrong - dice are ", str(dice), " but each count is not > 0?")
			return

		# get each new combination by iterating through every old combination + new die face
		for die_face in new_die.sides:
			for combo in small_pool.combo_mults:
				
				if ignore_dots:
					new_combo = (combo[0] + die_face.power,
						combo[1] + die_face.potential)
					
				else:
					new_combo = (combo[0] + die_face.power,
								combo[1] + die_face.potential,
								combo[2] + die_face.dots)

				if new_combo not in self.combo_mults:
					self.combo_mults[new_combo] = 0

				self.combo_mults[new_combo] += small_pool.combo_mults[combo]
				self.total_mult += small_pool.combo_mults[combo]

		dice_pool_dict[dice] = self

	def loadFromDict(self, dice_pool_dict, dice):
		self.combo_mults = dice_pool_dict(dice).combo_mults
		self.total_mult = dice_pool_dict(dice).total_mult

	def getSimpleDamage(self, kratos_pool):
		damage_dict = {}

		for symbol_pool, mult in self.combo_mults.items():
			damage_total = symbol_pool[0]

			breaks = kratos_pool.breaks
			fires = kratos_pool.fires
			hopes = kratos_pool.hopes

			potential = symbol_pool[1]
			dots = symbol_pool[2]

			# use breaks first
			converted = min(breaks, potential)
			damage_total += converted
			breaks -= converted
			potential -= converted

			# use hopes on dots
			converted = min(hopes, dots)
			damage_total += converted
			hopes -= converted
			dots -= converted #technically no longer necessary to keep track of this

			# use remaining hopes and fires
			converted = min(hopes, potential)
			damage_total += converted
			hopes -= converted
			potential -= converted

			converted = min(fires, potential)
			damage_total += converted
			fires -= converted
			potential -= converted

			if damage_total not in damage_dict:
				damage_dict[damage_total] = 0
			damage_dict[damage_total] += mult

		return damage_dict

	def DiceText(self):
		final = ""

		final += addStrPiece(final, ", ", self.dice[0], " reds")
		final += addStrPiece(final, ", ", self.dice[1], " blacks")
		final += addStrPiece(final, ", ", self.dice[2], " whites")

		if len(final) == 0:
			final += "no dice at all (why?)"

		return final

	def SymbolMultiplicityText(self):
		final = "If you roll " + self.DiceText() + ", then you have:\n"

		for result, mult in self.combo_mults.items():
			perc_str = str(round(mult * 100 / self.total_mult, 1)) + "%"

			# left-pad single-digit percents
			if mult / self.total_mult < 0.1:
				perc_str = " " + perc_str

			final += " > " + perc_str + " of\t" + formatDamageTuple(result) + "\n"

		return final

	def SimpleDamageText(self, kratos_pool):
		damage_dict = self.getSimpleDamage(kratos_pool)

		final = "If you roll " + self.DiceText() + ", and your Kratos table is"

		# conditional leading newline. "your Kratos table is empty" does not need a newline
		if not kratos_pool.isEmpty():
			final += "\n  "

		final += kratos_pool.PoolText() + "\nThen you have:\n"

		for damage, mult in sorted(damage_dict.items()):
			perc_str = str(round(mult * 100 / self.total_mult, 1)) + "%"

			# left-pad single-digit percents
			if mult / self.total_mult < 0.1:
				perc_str = " " + perc_str

			dmg_str = str(damage) + chr(int('3031', 16)) + " total"
			if damage < 10:
				dmg_str = " " + dmg_str

			final += " > " + perc_str + " of\t" + dmg_str + "\n"

		return final

class KratosPool():
	def __init__(self, brk=0, opn=0, div=0, fir=0, rse=0, blk=0, hop=0, cls=0):
		self.breaks = brk
		self.openings = opn
		self.diversions = div
		self.fires = fir
		self.rouses = rse
		self.blacks = blk
		self.hopes = hop
		self.closings = cls

	def isEmpty(self):
		return self.breaks + self.openings + self.diversions + self.fires + self.rouses + self.blacks + self.hopes + self.closings == 0

	def PoolText(self):
		if self.isEmpty():
			return "empty"

		table_text = ""

		table_text += addStrPiece(table_text, "\n  ", self.breaks, " breaks")
		table_text += addStrPiece(table_text, "\n  ", self.openings, " openings")
		table_text += addStrPiece(table_text, "\n  ", self.fires, " fires")
		table_text += addStrPiece(table_text, "\n  ", self.diversions, " diversions")
		table_text += addStrPiece(table_text, "\n  ", self.rouses, " rouses")
		table_text += addStrPiece(table_text, "\n  ", self.blacks, " blacks")
		table_text += addStrPiece(table_text, "\n  ", self.hopes, " hopes")
		table_text += addStrPiece(table_text, "\n  ", self.closings, " closings")

		return table_text

class Weapon():
	def __init__(self, na = "none", att_dice = 0, prec = 0, 
			  dice_per_hit = (0, 0, 0), flat_dice = (0, 0, 0), flat_pow = 0,
			  hit_dict = {}, traits = []):

		self.name = na
		self.attack_dice = att_dice
		self.precision = prec
		self.hit_dict = hit_dict

		if dice_per_hit != (0, 0, 0):
			for hits in range(1, att_dice + 1):
				hit = (hits * dice_per_hit[0] + flat_dice[0], 
				  	   hits * dice_per_hit[1] + flat_dice[1],
					   hits * dice_per_hit[2] + flat_dice[2],
					   flat_pow)

				if hits in hit_dict:
					print(na + ": kept " + str(hits) + " hit pool (" + str(hit_dict[hits]) + ") instead of calc value (" + str(hit))

class BPCard():
	def __init__(self, na = 'temp', AT = 0, goodness = {}, traits = []):
		self.name = na
		self.AT_base = AT

		self.fail = -1
		self.wound = 1
		self.crit = 1

		if 'hardened' in traits:
			self.crit -= 2