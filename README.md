# ss-to-kemis
Converts Survey Solutions export (tabular) to SQL statements for KEMIS

This takes a Survey Solutions export (tabular format, for TA and SLSS assessments) via stdin and returns on stdout SQL statements to insert the data into KEMIS

## Dependancies

 - python 2.7.x - www.python.org on Windows (uses [msvcrt](https://docs.python.org/2/library/msvcrt.html) module)

## Usage:

By itself, zipfile to sql:

 - `SS_TA_Completed.zip > python ImportAssessments.py > TA_Inserts.sql`

Or end to end:

 - `GetExport TA | python ImportAssessments.py | sqlcmd -d KEMIS`

## References:

 - GetExport - https://github.com/JeremyKells/SurveySolutionsAPI
 - sqlcmd    - https://msdn.microsoft.com/en-us/library/ms162773
