#!/usr/bin/python

import cgi
import urllib
import sys
import os
from pymongo import MongoClient
# import external classes based on relative file location
dir_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(dir_path, '../../../helpers'))
from Config import Config

def getMongoRecord(ensid, genome):
	dbConnection = Config(genome)
	gRNACollection = dbConnection.guideCollection
	guidesResult = gRNACollection.find({"ENSID": ensid})
	return guidesResult

def printGuides(guides, geneName):
	
	# only print table if there are guides
	if guides.count() > 0:
		print '''
		<table class="table table-bordered">
			<thead>
			<tr>
			<th class="centreCell" scope="col">Label <sup><i style="font-size: 13px;" class="fa fa-lock" onclick="unlockLabel(this)"></i></sup></th>
			<th scope="col">Sequence</th>
			<th scope="col">Location</th>
			<th class="centreCell" scope="col">Score</th>
			<th class="centreCell" scope="col">Off-Targets</th>
			<th class="centreCell" scope="col">Notes <sup><i style="font-size: 13px;" class="fa fa-lock" onclick="unlockNotes(this)"></i></sup></th>
			<th class="centreCell" id="acceptedGuideColumn" scope="col">Accepted</th>
			</tr>
			</thead>
			<tbody>
		'''
		for guideResult in guides:
			try:
				decodedNotes = urllib.unquote(guideResult['Notes']).decode("utf-8")
				decodedLabel = urllib.unquote(guideResult['label']).decode("utf-8")
				guideID, guideSeq, guideLocation, guideScore = str(guideResult['_id']), str(guideResult['guideSeq']), str(guideResult['guideLocation']), str(guideResult['guideScore'])
				encodedOffTarget = guideResult['otDesc'].encode("utf=8")
				print '''
				<tr id={guideID}>
				<td contenteditable="false" class="guideLabels" spellcheck="false" onblur="updateGuideLabel(this, '{guideID}')">{decodedLabel}</td>
				<td>{guideSeq}</td>
				<td style="white-space:nowrap;">{guideLocation}</td>
				<td class="centreCell">{guideScore}</td>
				<td class="centreCell">{encodedOffTarget}</td>
				<td style="padding: 0px;">
					<textarea disabled class="guideNotes" style="border:none; width: 100%; height: 75px; padding: 0px; vertical-align: middle;" onblur="updateGuideNote(this, '{guideID}')">{decodedNotes}</textarea>
				</td>
				'''.format(**locals())
				if str(guideResult['status']) == 'Accepted':
					print '''
					<td class="centreCell"><input type="checkbox" checked="checked" onclick="backendUpdateStatus(this, '{guideID}')">
					</td>'''.format(**locals())
				else:
					print '''<td class="centreCell"><input type="checkbox" onclick="backendUpdateStatus(this,'{guideID}')"></td>'''.format(**locals())
			except Exception, e:
				print str(e)
		print '''</tr></table>'''
	else:
		print "<p>No saved guides for " + str(geneName) + "</p>"


def main():
	print("Content-type: text/html\n")	
	
	try:
		args = cgi.FieldStorage()
		ensid = args.getvalue('ensid')
		genome = args.getvalue('genome')
		geneName = args.getvalue('geneName')
	except Exception, e:
		print "Error: " + str(e)
		return
	
	if not ensid or not genome:
		print("Error: missing required values for script (ensid or genome)")
		return
	
	guides = getMongoRecord(ensid, genome)
	printGuides(guides, geneName)


if __name__ == "__main__":
	main()
