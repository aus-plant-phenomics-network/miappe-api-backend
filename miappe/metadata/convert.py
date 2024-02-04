from miappe.metadata.isatools.model import *
from miappe.metadata.io import MetadataIO
import pandas as pd


def convert_ISA_tab(path: str, value_index: int = 3, validate: bool = True):
    # Read MIAPPE Metadata
    miappe_metadata = MetadataIO(path, value_index, validate)

    # Extract Miappe Frames
    miappe_investigation = miappe_metadata.frames['Investigation'].iloc[0, :]
    miappe_study = miappe_metadata.frames['Study']
    miappe_person = miappe_metadata.frames['Person']
    miappe_biological_material = miappe_metadata.frames['Biological Material']
    miappe_experimental_factor = miappe_metadata.frames['Experimental Factor']
    miappe_event = miappe_metadata.frames['Event']
    miappe_observation_unit = miappe_metadata.frames['Observation Unit']
    miappe_sample = miappe_metadata.frames['Sample']
    miappe_observed_variable = miappe_metadata.frames['Observed Variable']


class ISATabConverter:
    def __init__(self, miappe_investigation: pd.Series):
        self.miappe_investigation = miappe_investigation

    def create_investigation(self, investigation: pd.Series) -> Investigation:
        # Create ISA Tab items
        # Based on https://isa-tools.org/isa-api/content/examples/example-createSimpleISAtab.html
        # Field is populated using the mapping provided here
        # https://github.com/MIAPPE/MIAPPE/blob/master/MIAPPE_Checklist-Data-Model-v1.1/\
        # MIAPPE_mapping/MIAPPE_Checklist-1.1-with-mapping.pdf

        identifier = self.miappe_investigation['Investigation unique ID']
        title = self.miappe_investigation['Investigation title']
        description = self.miappe_investigation['Investigation description']
        submission_date = self.miappe_investigation['Submission date']
        public_release_date = self.miappe_investigation['Public release date']

        # Publication
        publications = Publication(doi=self.miappe_investigation['Associated publication'])

        # Investigation comments
        comment_license = Comment(name='License', value=self.miappe_investigation['License'])
        comment_miappe_version = Comment(name='MIAPPE version', value=self.miappe_investigation['MIAPPE version'])
        return Investigation(
            identifier=identifier,
            title=title,
            description=description,
            submission_date=submission_date,
            public_release_date=public_release_date,
            publications=publications,
            comments=[comment_license, comment_miappe_version]
        )

    def create_study(self, study: pd.Series, investigation: Investigation) -> Study:
        identifier = study['Study unique ID']
        title = study['Study title']
        description = study['Study description']

        # Study comments
        start_date = Comment(name='Start date of study',
                             value=study['Start date of study'])
        end_date = Comment(name='End date of study',
                           value=study['End date of study'])
        contact_institution = Comment(name="Contact institution",
                                      value=study['Contact institution'])
        country = Comment(name='Study Country',
                          value=study['Geographical location (country)'])
        experimental_site = Comment(name='Study Experimental Site',
                                    value=study['Experimental site name'])
        latitude = Comment(name='Study Latitude',
                           value=study['Geographic location (latitude)'])
        longitude = Comment(name='Study Longitude',
                            value=study['Geographic location (longitude)'])
        altitude = Comment(name='Study Altitude',
                           value=study['Geographic location (altitude)'])
