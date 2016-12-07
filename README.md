# ss-to-kemis
Converts Survey Solutions export (tabular) to SQL statements for KEMIS

This takes a Survey Solutions export (tabular format, for TA and SLSS assessments) via stdin and returns on stdout SQL statements to insert the data into KEMIS

## Usage:

By itself, zipfile to sql:

 - `SS_TA_Completed.zip > python ImportAssessments.py > TA_Inserts.sql`

Or end to end:

 - `GetExport TA | python ImportAssessments.py | sqlcmd -d KEMIS`

