
'''
#
# Purpose:
#
# Support routines for printing Editing Interface and other reports.
# These routines are used by all Python reports installed in
# titan:/export/mgd and other ad hoc Python reports.
#
# History:
#
#       lec     02/07/2000
#	- TR 1350; changes to copyright notice (trailer())
#
#       lec     12/06/1999
#	- TR 830; add parameters to init(), trailer() to format html output
#
#       cjd     12/07/1998
#       - added trailer() function
#
#	lec	11/16/98
#	- changed mgdreport to mgireport
#
#	lec	01/08/98
#	- converted to new mgdlib API
#	- added comments
#	- removed 'def sql()'; obsolete function 
#
'''

import sys
import string
import posix
import os
import mgdlib
import accessionlib

TAB = '\t'
CRT = '\n'
SEP = ', '
DOT = '.   '
SPACE = ' '
PAGE = ''
ULINE = '_'

column_width = 76	# Maximum column width
 
def init(outputfile, title = None, outputdir = None, printHeading = 1, isHTML = 0):
	'''
	# requires: outputfile, the name of the output file (string)
	#           title, the title of the report (string)
	#	    outputdir, the directory in which to place the output file (string)
	#	    isHTML, set to 1 if the output file is HTML format, 0 otherwise
	#
	# effects:
	# 1. Opens the output file under $HOME/mgireport directory for writing
	# 2. Initializes the output file with the title of the report, if given
	#
	# returns:
	# The file descriptor which was initialized
	#
	'''

	if isHTML:
		suffix = '.html'
	else:
		suffix = '.rpt'

	outputfile = os.path.splitext(outputfile)

	if outputdir is None:
		outputdir = os.environ['REPORTDIR']

	filename = outputdir + '/' + outputfile[0] + suffix

	fp = open(filename, 'w')

	if isHTML:
		fp.write("<HTML>")
		fp.write("<BODY>")
		fp.write("<PRE>")

	if printHeading:
		header(fp)

		if title is not None:
			fp.write(string.center(title, column_width) + 2 * CRT)

	return fp

def header(fp):
	'''
	# input: fp, output file descriptor pointing to an open file
	# effects: writes the standard MGI header to the file
	'''

	fp.write(
'''
The Jackson Laboratory - Mouse Genome Informatics - Mouse Genome Database (MGD)
Copyright 1996, 1999, 2000 The Jackson Laboratory
All Rights Reserved
Date Generated:  %s

''' % (mgdlib.date())
)

def trailer(fp):
	'''
	# input: fp, output file descriptor pointing to an open file
	# effects: writes the standard MGI warantee trailer to
	#  the output file file
	# notes: call this function just before closing. The trailers
	#  should be placed last in the file.
	'''
	fp.write(
'''
WARRANTY DISCLAIMER AND COPYRIGHT NOTICE
THE JACKSON LABORATORY MAKES NO REPRESENTATION ABOUT THE SUITABILITY OR 
ACCURACY OF THIS SOFTWARE OR DATA FOR ANY PURPOSE, AND MAKES NO WARRANTIES, 
EITHER EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY AND FITNESS FOR A 
PARTICULAR PURPOSE OR THAT THE USE OF THIS SOFTWARE OR DATA WILL NOT 
INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS, OR OTHER RIGHTS.  
THE SOFTWARE AND DATA ARE PROVIDED "AS IS".

This software and data are provided to enhance knowledge and encourage 
progress in the scientific community and are to be used only for research 
and educational purposes.  Any reproduction or use for commercial purpose 
is prohibited without the prior express written permission of the Jackson 
Laboratory.

Copyright © 1996, 1999, 2000 by The Jackson Laboratory
'''
)

	return


def finish_nonps(fp, isHTML = 0):
	'''
	# requires: fp, the output file descriptor
	#
	# effects:
	# 1. Closes the output file
	#
	# returns:
	#
	'''

	if isHTML:
		fp.write("</PRE>")
		fp.write("</BODY>")
		fp.write("</HTML>")

	fp.close()
 
def finish_ps(fp, banner = None, options = None):
	'''
	# requires: fp, the output file descriptor
	#           banner, a banner to print (string)
	#           options, a list of  postscript options (string)
	#
	# effects:
	# 1. Closes the open output file
	# 2. Creates and prints a postscript file of the output file
	#    by opening a pipe to a postscript conversion program 'enscript'
	#
	# returns:
	#
	'''

	filename = fp.name
	file = fp.name + '.ps'
	fp.close()
 
        cmd = 'rsh uncompaghre "set path = ($path /usr/local/bin);enscript -b"'
	
	if banner != None:
              cmd = cmd + banner 

	if options != None:
              cmd = cmd + options

	cmd = cmd + '" -fTimes-Roman8 -p' + file + ' ' + filename + '"'
        p = posix.popen(cmd, 'r')
        s = p.read()
        p.close()

def format_line(str):
	'''
	# requires: str, the line to format (string)
	#
	# effects:
	# Inserts carriage returns and tabs into a string
	# if it is greater than the global column_width.
	# If the length of the string is less than or equal 
	# to the global column_width then
	# no changes to the string are necessary.
	#
	# returns:
	# The converted or unchanged string.
	#
	'''

        newstr = ''
        counter = len(str) / column_width
 
        start = 0
        end = column_width - 1
 
        while (counter):
                newstr = newstr + str[start : end + 1] + CRT + TAB
                start = start + column_width
                end = start + column_width - 1
                counter = counter - 1
 
        newstr = newstr + str[start : ]
        return newstr
 
def process_ref(fp, command, whichFormat = 1):
	'''
	# requires: fp, the output file descriptor
	#	    command, the SQL command to execute (string)
	#		This command is expected to return the _Refs_key
	#		of each returned record.  Other columns may be
	#		returned, but _Refs_key MUST be returned.
	#	    whichFormat, the format to use (1,2,3)
	#	    1 prints author, citation, title, jnum, UI, datasets
	#	    2 prints author, title, citation, jnum, datasets
	#	    3 prints author, title, citation, jnum, datasets plus abstract
	#
	# effects:
	# 1. Executes the SQL command and writes the results
	#    to the output file specified.
	#
	# returns:
	#
	'''

	row = 1

	# At a minimum, the command must return a list of _Refs_keys
	results = mgdlib.sql(command, 'auto')

	for result in results:
		command = 'select * from BIB_All_View where _Refs_key = %d' % result['_Refs_key']
		references = mgdlib.sql(command, 'auto')

		for ref in references:	# Should be only one

       			authors = `row` + DOT + TAB + mgdlib.prvalue(ref['authors']) + SEP + CRT

        		if len(authors) > column_width:
                		authors = format_line(authors)
 
        		title = TAB + mgdlib.prvalue(ref['title']) + CRT
 
        		if len(title) > column_width:
                		title = format_line(title)
 
        		citation = TAB + mgdlib.prvalue(ref['citation']) + CRT
       			jnum = TAB + mgdlib.prvalue(ref['jnumID']) + CRT
       			dbs = TAB + mgdlib.prvalue(ref['dbs']) + CRT

			ui = accessionlib.get_accID(ref['_Refs_key'], "Reference", "Medline")

			if ui is None:
				ui = ''
			else:
				ui = TAB + ui + CRT

			if whichFormat == '1':
				fp.write(authors + citation + title + jnum + ui + dbs + CRT)
			else:
				fp.write(authors + title + citation + jnum + dbs + CRT)
		
        		cmd = 'select note from BIB_Notes where _Refs_key = %d order by sequenceNum' % ref['_Refs_key']
        		notes = mgdlib.sql(cmd, 'auto')

			for note in notes:
				n = TAB + note['note']
				if len(n) > column_width:
					n = format_line(n)

				fp.write(n + CRT + CRT)

			if whichFormat == '3':
        			cmd = 'select abstract from BIB_Refs where _Refs_key = %d' % ref['_Refs_key']
				abstract = mgdlib.sql(cmd, 'auto')

				for abs in abstract:
					a = TAB + mgdlib.prvalue(abs['abstract'])
					if len(a) > column_width:
						a = format_line(a)

					fp.write(a + CRT + CRT)
 
        		row = row + 1
 
