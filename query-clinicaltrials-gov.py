#!/usr/bin/env python3

import requests
import argparse
from urllib import parse

'''
Query clinicaltrials.gov:

*  Get total number of subjects for some sponsor, location, and study status.
*  Get number of studies for some sponsor, location, study type, and study status.

See the documentation:

*  https://www.clinicaltrials.gov/api/
*  https://www.clinicaltrials.gov/api/gui/ref/crosswalks

Example query as URL: 

https://www.clinicaltrials.gov/api/query/field_values?expr=SEARCH%5BLocation%5D%28AREA%5BLocationFacility%5DNIH+Clinical+Center%29&field=OutcomeDenomCountValue&fmt=json

Equivalent to: SEARCH[Location](AREA[LocationFacility]NIH Clinical Center)

Query Field Values:

*  Name of the sponsor: LeadSponsorName (e.g. "NINDS")
*  Facility name: LocationFacility (e.g. "NIH Clinical Center")
*  Study type: StudyType (e.g. "Interventional", "Observational") 
*  Study status: OverallStatus:
    Not yet recruiting: Participants are not yet being recruited
    Recruiting: Participants are currently being recruited, whether or not any participants have yet been enrolled
    Enrolling by invitation: Participants are being (or will be) selected from a predetermined population
    Active, not recruiting: Study is continuing, meaning participants are receiving an intervention or being examined, but new participants are not currently being recruited or enrolled
    Completed: The study has concluded normally; participants are no longer receiving an intervention or being examined (that is, last participant’s last visit has occurred)
    Suspended: Study halted prematurely but potentially will resume
    Terminated: Study halted prematurely and will not resume; participants are no longer being examined or receiving intervention
    Withdrawn: Study halted prematurely, prior to enrollment of first participant

Field:

*  Number of Participants Analyzed: EnrollmentCount

Example:

./query-clinicaltrials-gov.py --field EnrollmentCount --sponsors NCI NEI NHLBI NHGRI NIA NIAAA NIAID NIAMS NIBIB NICHD NIDCD NIDCR NIDDK NIDA NIEHS NIGMS NIMH NIMHD NINDS NINR NCCIH NCATS CC NLM CSR CIT FIC

'''

parser = argparse.ArgumentParser()
parser.add_argument('--sponsors', required=True, nargs='+', help="Sponsors of Choice")
parser.add_argument('--field', required=True, help="Field to count - case sensitive (EnrollmentCount | StudyType)")
parser.add_argument('--status', default='Completed', help="Study status")
parser.add_argument('--location', default='NIH Clinical Center', help="Study location")
args = parser.parse_args()

baseurl = 'https://www.clinicaltrials.gov/api/query/field_values?'
exampleurl = 'https://www.clinicaltrials.gov/api/query/field_values?expr=SEARCH%5BLocation%5D%28AREA%5BLocationFacility%5DNIH+Clinical+Center%29&field=EnrollmentCount&fmt=json'

def main():
    baseUrl = "https://www.clinicaltrials.gov/api/query/field_values?expr={SEARCH}&field={field}&fmt=json"
    for sponsor in args.sponsors:
        query = "AREA[LocationFacility]{LOCATION} AND AREA[OverallStatus]{STATUS} AND AREA[LeadSponsorName]{SPONSOR}".format(LOCATION=args.location, STATUS=args.status, SPONSOR=sponsor)
        urlEncodedQuery = parse.quote(query)
        queryUrl = baseUrl.format(SEARCH=urlEncodedQuery,field=args.field)
        response = requests.get(queryUrl)
        response.raise_for_status()
        jsonResponse = response.json()

        if args.field == "EnrollmentCount": 
            countFieldValues = jsonResponse["FieldValuesResponse"]["FieldValues"]
            totalCount = 0
            for value in countFieldValues:
                totalCount += int(value["FieldValue"])*int(value["NStudiesFoundWithValue"])
        
            print("{SPONSOR}\t{STATUS}\t{LOCATION}\t{COUNT}".format(SPONSOR=sponsor, STATUS=args.status, LOCATION=args.location, COUNT=totalCount))

        elif args.field == "StudyType":
            studies = jsonResponse["FieldValuesResponse"]["FieldValues"]
            for study in studies:
                studytype= study["FieldValue"]
                nstudies = study["NStudiesFoundWithValue"]
                print("{SPONSOR}\t{STUDYTYPE}\t{STATUS}\t{LOCATION}\t{STUDIES}".format(SPONSOR=sponsor, STUDYTYPE=studytype, STUDIES=nstudies, STATUS=args.status, LOCATION=args.location)) 

if __name__ == "__main__":
    main()
