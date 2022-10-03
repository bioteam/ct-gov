#!/usr/bin/env python3

import requests
import argparse
from urllib import parse

'''
Query clinicaltrials.gov:

* EnrollmentCount - get total number of subjects for sponsor, location, and status.
* StudyType - Get number of studies of some type (Interventional, Observational).

See the documentation:

* https://www.clinicaltrials.gov/api/
* https://www.clinicaltrials.gov/api/gui/ref/crosswalks

Example query as URL:

https://www.clinicaltrials.gov/api/query/field_values?expr=SEARCH%5BLocation%5D%28AREA%5BLocationFacility%5DNIH+Clinical+Center%29&field=OutcomeDenomCountValue&fmt=json

Equivalent to: SEARCH[Location](AREA[LocationFacility]NIH Clinical Center)

Query Field Values:

* Name of the sponsor: LeadSponsorName (e.g. "NINDS")
* Facility name: LocationFacility (e.g. "NIH Clinical Center")
* Study type: StudyType (e.g. "Interventional", "Observational")
* Study status: OverallStatus:
    * Completed: The study has concluded normally; participants are no longer
                 receiving an intervention or being examined
    * Recruiting: Participants are currently being recruited, whether or not
                  any participants have yet been enrolled
    * Active, not recruiting: Study is continuing, meaning participants are
                              receiving an intervention or being examined
    * Enrolling by invitation: Participants are being (or will be) selected
                               from a predetermined population
    * Not yet recruiting: Participants are not yet being recruited
    * Suspended: Study halted prematurely but potentially will resume
    * Terminated: Study halted prematurely and will not resume; participants
                  are no longer being examined or receiving intervention
    * Withdrawn: Study halted prematurely, prior to enrollment of first
                 participant

Example:

./query-clinicaltrials-gov.py --field EnrollmentCount --sponsors NCI NEI \
                           NHLBI NHGRI NIA NIAAA NIAID NIAMS NICHD NIDCD \
                           NIDCR NIDDK NIDA NIMH NINDS NINR NCCIH CC

No trials as of 9/2022: NIBIB, NIGMS, NIMHD, NCATS, NIEHS

'''

parser = argparse.ArgumentParser()
parser.add_argument('--sponsors', required=True,
                    nargs='+', help="Sponsors of Choice")
parser.add_argument('--field', required=True,
                    help="Field to count: EnrollmentCount or StudyType")
parser.add_argument('--status',
                    default='Completed', help="Study status")
parser.add_argument('--location',
                    default='NIH Clinical Center', help="Study location")
args = parser.parse_args()


def main():
    baseUrl = "https://www.clinicaltrials.gov/api/query/field_values?expr={SEARCH}&field={FIELD}&fmt=json"
    for sponsor in args.sponsors:
        query = "AREA[LocationFacility]{LOCATION} AND AREA[OverallStatus]{STATUS} AND AREA[LeadSponsorName]{SPONSOR}".format(
            LOCATION=args.location, STATUS=args.status, SPONSOR=sponsor)
        urlEncodedQuery = parse.quote(query)
        queryUrl = baseUrl.format(SEARCH=urlEncodedQuery, FIELD=args.field)
        response = requests.get(queryUrl)
        response.raise_for_status()
        results = response.json()["FieldValuesResponse"]["FieldValues"]

        if args.field == "EnrollmentCount":
            totalCount = 0
            for result in results:
                totalCount += int(result["FieldValue"]) * \
                    int(result["NStudiesFoundWithValue"])
                # print("{SPONSOR}\t{STATUS}\t{LOCATION}\t{COUNT}".format(SPONSOR=sponsor, STATUS=args.status, LOCATION=args.location, COUNT=result["FieldValue"]))
            print("{SPONSOR}\t{STATUS}\t{LOCATION}\t{COUNT}".format(
                SPONSOR=sponsor, STATUS=args.status, LOCATION=args.location, COUNT=totalCount))

        elif args.field == "StudyType":
            for result in results:
                print("{SPONSOR}\t{STUDYTYPE}\t{STATUS}\t{LOCATION}\t{STUDIES}".format(
                    SPONSOR=sponsor, STUDYTYPE=result["FieldValue"], STUDIES=result["NStudiesFoundWithValue"], STATUS=args.status, LOCATION=args.location))


if __name__ == "__main__":
    main()
