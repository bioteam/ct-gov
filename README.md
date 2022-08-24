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

