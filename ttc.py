import numpy as np

class Market:
	def __init__(self, name, ordered_students, rooms):
		self.name = name
		self.students = ordered_students
		self.rooms = rooms

	def __repr__(self):
		self_str = self.name+"\n------------------------\n"
		self_str += "Rooms %s\n------------------------\n" % self.rooms
		for s in self.students:
			self_str += (str(s) + "\n")
		return self_str

	def is_valid(self):
		occupied = set()
		for s in self.students:
			if s.endowment:
				if s.endowment in occupied:
					print ">1 student in %s's room!" % s.name
					return False
				if s.endowment not in self.rooms:
					print "%s's endowment not a valid room!" % s.name
					return False
				if s.endowment not in s.prefs:
					print "%s's endowment is not in his preferences!" % s.name
					return False
			if not set(s.prefs).issubset(set(self.rooms)):
				print "%s's prefs has an invalid room!" % s.name
				return False
			occupied.add(s.endowment)

		return True

	def fill_prefs(self):
		for s in self.students:
			if (s.endowment is None) and (len(s.prefs) < len(self.rooms)):
				remain = set(self.rooms).difference(set(s.prefs))
				s.prefs += set(remain)

	def best_remaining(self, student, taken):
		for room in student.prefs:
			if room not in taken:
				return room
		return None

	def get_owner(self, room):
		if room == None:
			return None
		else:
			for s in self.students:
				if s.endowment == room:
					return s
		return None

	def is_IR(self, allocation):
		for s in self.students:
			if not s.is_IR(allocation[s]):
				return False
		return True

	def yrmh_igyt(self):
		allocation = {}
		priority = self.students
		temp = []
		log = ""

		while len(priority) > 0:
			# print "--------------------------------"
			# print "priority", priority
			s = priority[0]

			top = self.best_remaining(s, allocation.values())
			owner = self.get_owner(top)	
			log += "%s wants %s, owned by %s\n" % (s.name, top, (owner.name if owner else "None"))

			# print "s", s
			# print "top", top
			# print "owner", owner
			# print "temp", temp

			if (owner is None) or (owner==s) or (owner in allocation):
				allocation[s] = top
				priority = priority[1:]
				log += "%s: %s->%s\n" % (("EMPTY" if not owner 
					else ("SQUAT" if owner==s else "INHERIT")), s.name, top)

			elif owner in temp:
				ix = temp.index(owner)
				cycle = temp[ix:]+[s]
				for i in range (0,len(cycle)):
					cur = cycle[i]
					ctop = cycle[(i+1)%len(cycle)].endowment
					allocation[cur] = ctop
					log += "CYCLE: %s->%s\n" % (cur.name, ctop)

				temp = temp[:ix]
				priority = priority[len(cycle):]

			else:
				if s not in temp:
					temp.append(s) 
				ix = priority.index(owner)
				priority = [owner] + priority[:ix] + priority[ix+1:] 

		return allocation, log



class Student:
	def __init__(self, name, endowment, prefs):
		self.name = name
		self.endowment = endowment
		self.prefs = prefs

	def __repr__(self):
		pref_str = str(self.prefs[0])
		for p in self.prefs[1:]:
			pref_str += (" > %s" % p)
		if self.endowment:
			return "(%s, %s)  %s" % (self.name, self.endowment, pref_str)
		else:
			return "(%s, None)  %s" % (self.name, pref_str)

	def is_IR(self, room):
		return (self.endowment is None) or self.prefs.index(room) <= self.prefs.index(self.endowment)
