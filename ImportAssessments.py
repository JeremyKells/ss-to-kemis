import os, sys, msvcrt
import StringIO
import csv
import os
import re
from zipfile import ZipFile

def processFile(archive, assessmentType):

    
    assessments = {'TA': 'Teacher Performance Appraisal', 'SLSS': 'School Leader Performance Appraisal'}
    with archive.open('%s.do' % assessments[assessmentType]) as doFile:
        schoolsline = [l for l in doFile.readlines() if l.startswith('label define lschool')][0]
        schools = dict(re.findall(r'''(\d*)[ ][`]["](.*?)["]''', schoolsline))


    print "SET QUOTED_IDENTIFIER ON"
    print "SET XACT_ABORT ON"
    print "declare @paID int"

    with archive.open('%s.tab' % assessments[assessmentType]) as tabfile:
        records = csv.DictReader(tabfile, delimiter='\t')
        for record in records:
            print "BEGIN TRANSACTION"
            tID = record['interviewee']
            schoolName = schools[record['school'].split('.')[0]]

            print "INSERT INTO paAssessment_ (tID, paSchNo, paDate, pafrmCode) " + \
                  "SELECT %s, schNo, '%s', '%s' FROM Schools WHERE schName = '%s'" % (
                                         tID,
                                         record['date'],
                                         assessmentType,
                                         schoolName)

            print "select @paID = scope_identity()"
            for key in records.fieldnames:
                value = record[key]
                if key.startswith(assessmentType):
                    val = {'0': "'N'", '1': "'Y'", '-999999999': "'X'"}
                    print "INSERT INTO paAssessmentLine_ (paID, paindID, paplCode ) " + \
                          "Select @paID, paIndID, %s from paIndicators " % val[value] + \
                          "WHERE indFullID = '%s' " % key.replace('__', '.').replace('_', '.')
            print "COMMIT TRANSACTION"

if __name__ == "__main__":

    msvcrt.setmode (sys.stdin.fileno(), os.O_BINARY)
    input = sys.stdin.read()
    archive = ZipFile(StringIO.StringIO(input))
    assessmentType = None
    assessmentType = 'TA' if 'Teacher Performance Appraisal.tab' in archive.namelist() else assessmentType
    assessmentType = 'SLSS' if 'School Leader Performance Appraisal.tab' in archive.namelist() else assessmentType
    if assessmentType is None:
        print 'Invalid File input'
    else:
        processFile(archive, assessmentType)
