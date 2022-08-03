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
*  Study status: OverallStatus (e.g. "Completed")
*  Facility name: LocationFacility (e.g. "NIH Clinical Center")
*  Study type: StudyType (e.g. "Interventional", "Observational") 

Field:

*  Number of Participants Analyzed: EnrollmentCount

'''

parser = argparse.ArgumentParser()
parser.add_argument('--sponsor', required=True, help="Sponsor of Choice")
parser.add_argument('--field', required=True, help="Field to count - case sensitive (EnrollmentCount | StudyType)")
args = parser.parse_args()

baseurl = 'https://www.clinicaltrials.gov/api/query/field_values?'
exampleurl = 'https://www.clinicaltrials.gov/api/query/field_values?expr=SEARCH%5BLocation%5D%28AREA%5BLocationFacility%5DNIH+Clinical+Center%29&field=EnrollmentCount&fmt=json'


# input: sponsor param 
# output: Number of participants at the clinical center [--location param] filtered by sponsor [--sponsor param]

def main():
    baseUrl = "https://www.clinicaltrials.gov/api/query/field_values?expr={SEARCH}&field={field}&fmt=json"
    query = "AREA[LocationFacility]NIH Clinical Center AND AREA[OverallStatus]Recruiting AND AREA[LeadSponsorName]{SPONSOR}".format(SPONSOR = args.sponsor)
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
        
        print("Total Participants found in {SPONSOR}: {COUNT}".format(SPONSOR = args.sponsor, COUNT = totalCount))

    elif args.field == "StudyType":
        studies = jsonResponse["FieldValuesResponse"]["FieldValues"]
        for study in studies:
            studytype= study["FieldValue"]
            nstudies = study["NStudiesFoundWithValue"]
            print("Number of {STUDYTYPE} Studies found in {SPONSOR}: {STUDIES}".format(SPONSOR = args.sponsor, STUDYTYPE = studytype, STUDIES = nstudies)) 

"""-- query "AREA[LocationFacility]NIH Clinical Center AND AREA[OverallStatus]Completed AND AREA[LeadSponsorName]NEI" """

if __name__ == "__main__":
    main()