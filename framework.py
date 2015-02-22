id_list={}
statements=[]
class Description:
	"""
		Class that ensures that descriptions in the \"YouAreInARoom\" model fit the state supplied by a user.
	"""
	def __init__(self, description, global_state, requirements={}):
		"""
			Initialises a Description class, storing the given description and making a copy of the global state, modified to suit the requirements proffered.
		"""
		self.description=description
		self.requirements={}
		self.requirements.update(global_state)
		self.requirements.update(requirements)
	def describe(self, state):
		"""
			Attempts to print a description, if and only if the supplied state matches the requirements stated during initialisation. Otherwise, returns None.
		"""
		try:
			if all([ self.requirements[key]==state[key] for key in self.requirements ]):
				return description
			else:
				return None
		except:
			raise Exception("Expected key \""+key+"\" was (probably) not found in STATE dict! This is pretty serious!")

class Interaction:
	"""
		This class manages the interactions themselves, their responses and how they change states.
	"""
	def __init__(self, statement, response, changes={}):
		"""
			Simple initialisation, storing the values directly to the attribute.
		"""
		self.statement=statement
		self.response=response
		self.changes=changes
	def save(self, database):
		"""
			This saves the interaction data to a database
		"""
		raise Exception("THIS HAS NOT BEEN IMPLEMENTED")

class Interactors:
	"""
		Class that abstracts things that can be interacted with in the "YouAreInARoom" model
	"""
	def __init__(self, id, nicks=[], descriptions=[]):
		"""
			Initialses the Interactor class
		"""
		if id in id_list:	
			raise Exception("id \""+id+"\" already in use")
		id_list[id]=self
		self.__id=id
		# this is not being used yet, but could be good if we turn interactions into regex based searches
		self.__nicks=nicks
		#
		self.__descriptions=descriptions
		self.__interactions=[]
		self.__children=[]
	def search_interactions(self, statement):
		"""
			Searches the current Interactor and it's children for matches to the supplied statement, and returns the interaction.
		"""
		for interaction in self.__interactions.items():
			if statement == interaction.statement:
				return self.__interactions[interaction]
		for child in self.__children:
			interaction=child.search_interactions(statement)
			if interaction: return interaction
		return None	
	def add_interaction(self, interaction):
		"""
			Checks that 'interaction' variable is of the Interaction class, and adds it to the interactions of the interactor if that is the case.
		"""
		if isinstance(interaction,Interaction):
			self.__interactions+=[interaction]
		else:
			raise Exception("Somebody attempted to add an interaction that wasn't of the bleeming Interaction class I wrote. Jerks")

	def add_description(self, description):
		"""
			Checks that 'description' variable is of the Description class, and adds it to the descriptions of the interactor if that is the case.
		"""
		if isinstance(description, Description):
			self.__descriptions+=[description]
		else:
			raise Exception("Somebody attempted to add a description that wasn't the bloody Description class I wrote. Feckers")

	def describe(self, state={}):
		"""
			Returns the first description that matches the given state, or None.
		"""
		output=None
		for description in self.__descriptions:
			output=description.describe(state)	
			if output: break
		return output	

	def interact(self, statement, state={}):
		"""
			This function searches for previous interactions, and returns the response. If there is no instance of the previous responses, requests human interaction.
		"""
		interaction=search_interactions(statement)
		if interaction:
			return (interaction.response, state.update(interaction.changes))
		else:
			ask_for_help(statement, self.id)
			return None	

	def save(self, filepath):
		"""
			Saves the interactions stored in this Interactor to a database at filepath"
		"""
		raise Exception("THIS HAS NOT BEEN IMPLEMENTED")

	def load(self, filepath):
		"""
			Loads the interactions stored in the database at filepath, that relate to this Interactor.
		"""
		raise Exception("THIS HAS NOT BEEN IMPLEMENTED")


def load(path):
	"""
		Load stored Interactors from a file
	"""
	return (None, None)
	
