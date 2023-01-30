#!/usr/bin/env python2

##https://github.com/josh-newton/secret-santa-generator/blob/master/generate.py

import random

givers = [
'Mark',
'Mary',
'Melissa',
'Analie',
'Marta',
'Arlene',
'Erik'
]
excludes = {

}

def genSecretSanta():
	result = []
	restart = True

	while restart:
		restart = False
		receivers = givers[:]

		for i in range(len(givers)):
			giver = givers[i]
			# Pick a random reciever
			receiver = random.choice(receivers)

			# If we've got to the last giver and its the same as the reciever, restart the generation
			if (giver == receiver and i == (len(givers) - 1)):
				restart = True
				break
			else:
				# Ensure the giver and reciever are not the same, and they are not in the excludes list
				while (receiver == giver) or (receiver in excludes and giver == excludes[receiver]):
					receiver = random.choice(receivers)
				# Add result to array
				result.append(giver + ' gives to ' + receiver)
				# Remove the reciever from the list
				receivers.remove(receiver)

	for r in result:
		print (r)

def main():
	genSecretSanta()

if __name__ == '__main__':
	main()