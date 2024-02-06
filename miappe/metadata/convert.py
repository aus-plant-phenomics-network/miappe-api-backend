import pandas as pd

from miappe.metadata.isatools.model import Investigation, Person, Publication, Comment, Study, StudyFactor, \
    Characteristic, Protocol, ProtocolParameter, Sample, FactorValue, Extract, ParameterValue, Source, \
    OntologyAnnotation


class ISATabConverter:
    def __init__(self,
                 miappe_investigation: pd.Series,
                 miappe_study: pd.DataFrame):
        self.miappe_investigation = miappe_investigation
        self.miappe_study = miappe_study

        self.isa_investigation = self.create_investigation(self.miappe_investigation)
        self.isa_studies = {}
        self.isa_people = {}

    @staticmethod
    def get_study_ids(id_str: str) -> list[str]:
        return [item.strip() for item in id_str.split(";")]

    @staticmethod
    def create_investigation(miappe_investigation: pd.Series) -> Investigation:
        # Create ISA Tab items
        # Based on https://isa-tools.org/isa-api/content/examples/example-createSimpleISAtab.html
        # Field is populated using the mapping provided here
        # https://github.com/MIAPPE/MIAPPE/blob/master/MIAPPE_Checklist-Data-Model-v1.1/\
        # MIAPPE_mapping/MIAPPE_Checklist-1.1-with-mapping.pdf

        identifier = miappe_investigation['Investigation unique ID']
        title = miappe_investigation['Investigation title']
        description = miappe_investigation['Investigation description']
        submission_date = miappe_investigation['Submission date']
        public_release_date = miappe_investigation['Public release date']

        # Publication
        publications = Publication(doi=miappe_investigation['Associated publication'])

        # Investigation comments
        comment_license = Comment(name='License', value=miappe_investigation['License'])
        comment_miappe_version = Comment(name='MIAPPE version', value=miappe_investigation['MIAPPE version'])
        investigation_comments = [comment_license, comment_miappe_version]
        return Investigation(
            identifier=identifier,
            title=title,
            description=description,
            submission_date=submission_date,
            public_release_date=public_release_date,
            publications=publications,
            comments=investigation_comments,
            studies=[]
        )

    @staticmethod
    def create_study(miappe_study: pd.Series) -> Study:
        identifier = miappe_study['Study unique ID']
        filename = f"s_{identifier}.txt"
        title = miappe_study['Study title']
        description = miappe_study['Study description']

        # Study comments
        start_date = Comment(name='Start date of study',
                             value=miappe_study['Start date of study'])
        end_date = Comment(name='End date of study',
                           value=miappe_study['End date of study'])
        contact_institution = Comment(name="Contact institution",
                                      value=miappe_study['Contact institution'])
        country = Comment(name='Study Country',
                          value=miappe_study['Geographic location (country)'])
        experimental_site = Comment(name='Study Experimental Site',
                                    value=miappe_study['Experimental site name'])
        latitude = Comment(name='Study Latitude',
                           value=miappe_study['Geographic location (latitude)'])
        longitude = Comment(name='Study Longitude',
                            value=miappe_study['Geographic location (longitude)'])
        altitude = Comment(name='Study Altitude',
                           value=miappe_study['Geographic location (altitude)'])
        study_comments = [
            start_date,
            end_date,
            contact_institution,
            country,
            experimental_site,
            latitude,
            longitude,
            altitude
        ]

        # Study Design Comments
        design_description = Comment(name='Study Design Description',
                                     value=miappe_study['Description of the experimental design'])
        study_design_type = miappe_study['Type of experimental design']
        observation_unit_level_hierarchy = Comment(name='Observation Unit Level Hierarchy',
                                                   value=miappe_study['Observation unit level hierarchy'])
        observation_unit_description = Comment(name='Observation Unit Description',
                                               value=miappe_study['Observation unit description'])
        description_of_growth_facility = Comment(name='Description of Growth Facility',
                                                 value=miappe_study['Description of growth facility'])
        type_of_growth_facility = Comment(name='Type of Growth Facility',
                                          value=miappe_study['Type of growth facility'])
        map_of_experimental_design = Comment(name='Map of Experimental Design',
                                             value=miappe_study['Map of experimental design'])
        study_design_comments = [
            design_description,
            observation_unit_level_hierarchy,
            observation_unit_description,
            description_of_growth_facility,
            type_of_growth_facility,
            map_of_experimental_design
        ]
        study_design_description = OntologyAnnotation(
            term_accession=study_design_type,
            comments=study_design_comments
        )

        # Study Protocol
        cultural_practices = Protocol(
            name="Growth",
            description=miappe_study['Cultural practices'])
        return Study(
            filename=filename,
            identifier=identifier,
            title=title,
            description=description,
            design_descriptors=[study_design_description],
            protocols=[cultural_practices],
            comments=study_comments,
            contacts=[],
            sources=[],
            factors=[],
            samples=[]
        )

    @staticmethod
    def create_person(miappe_person: pd.Series) -> Person:
        name = miappe_person['Person name']
        email = miappe_person['Person email']
        id_ = miappe_person['Person ID']
        role = [miappe_person['Person role']]
        affiliation = miappe_person['Person affiliation']
        return Person(
            id_=id_,
            first_name=name,
            email=email,
            roles=role,
            affiliation=affiliation
        )

    @staticmethod
    def create_data_file(miappe_data_file: pd.Series) -> list[Comment]:
        return [
            Comment(name="Study Data File Link", value=miappe_data_file['Data file link']),
            Comment(name="Study Data File Description", value=miappe_data_file['Data file description']),
            Comment(name="Study Data File Version", value=miappe_data_file['Data file version']),
        ]

    @staticmethod
    def create_biological_material(miappe_biological_material: pd.Series) -> Source:
        name = miappe_biological_material['Biological material ID']
        organism = Characteristic(category='Organism', value=miappe_biological_material['Organism'])
        genus = Characteristic(category='Genus', value=miappe_biological_material['Genus'])
        species = Characteristic(category="Species", value=miappe_biological_material['Species'])
        infra_name = Characteristic(category="Infraspecific Name",
                                    value=miappe_biological_material['Infraspecific name'])
        bio_lat = Characteristic(category="Biological Material Latitude",
                                 value=miappe_biological_material["Biological material latitude"])
        bio_long = Characteristic(category="Biological Material Longitude",
                                  value=miappe_biological_material["Biological material longitude"])
        bio_alt = Characteristic(category="Biological Material Altitude",
                                 value=miappe_biological_material["Biological material altitude"])
        bio_uncertainty = Characteristic(category='Biological Material Coordinates Uncertainty',
                                         value=miappe_biological_material[
                                             'Biological material coordinates uncertainty'])
        bio_material_preproc = Characteristic(category="Biological Material Preprocessing",
                                              value=miappe_biological_material['Biological material preprocessing'])
        material_source_id = Characteristic(category="Material Source ID",
                                            value=miappe_biological_material[
                                                "Material source ID (Holding institute/stock centre, accession)"])
        material_source_doi = Characteristic(category="Material Source DOI",
                                             value=miappe_biological_material["Material source DOI"])
        material_lat = Characteristic(category="Material Source Latitude",
                                      value=miappe_biological_material["Material source latitude"])
        material_long = Characteristic(category="Material Source Longitude",
                                       value=miappe_biological_material["Material source longitude"])
        material_alt = Characteristic(category="Material Source Altitude",
                                      value=miappe_biological_material['Material source altitude'])
        material_uncertainty = Characteristic(category='Material Source Coordinates Uncertainty',
                                              value=miappe_biological_material[
                                                  'Material source coordinates uncertainty'])
        material_source_description = Characteristic(category="Material Source Description",
                                                     value=miappe_biological_material['Material source description'])
        characteristics = [
            organism,
            genus,
            species,
            infra_name,
            bio_lat,
            bio_long,
            bio_alt,
            bio_uncertainty,
            bio_material_preproc,
            material_source_id,
            material_source_doi,
            material_lat,
            material_long,
            material_alt,
            material_uncertainty,
            material_source_description
        ]
        return Source(
            name=name,
            characteristics=characteristics
        )

    @staticmethod
    def create_environment(miappe_environment: pd.Series) -> dict:
        return {
            "name": ProtocolParameter(
                parameter_name=miappe_environment['Environment parameter']
            ),
            "value": ParameterValue(
                value=miappe_environment['Environment parameter value']
            )
        }

    @staticmethod
    def create_experimental_factor(miappe_experimental_factor: pd.Series) -> StudyFactor:
        name = miappe_experimental_factor['Experimental Factor type']
        description = Comment(name="Study Factor Description",
                              value=miappe_experimental_factor['Experimental Factor description'])
        values = Comment(name="Study Factor Values",
                         value=miappe_experimental_factor['Experimental Factor values'])
        factor_comments = [description, values]
        return StudyFactor(
            name=name,
            comments=factor_comments
        )

    @staticmethod
    def create_event(miappe_event: pd.Series) -> Protocol:
        # TODO: add value to event file
        return Protocol(
            name=miappe_event['Event type'],
            protocol_type="Event",
            uri=miappe_event['Event accession number'],
            description=miappe_event['Event description']
        )

    @staticmethod
    def create_observation_unit(miappe_observation_unit: pd.Series) -> Sample:
        unit_type = Characteristic(category='Observation Unit Type',
                                   value=miappe_observation_unit['Observation unit type'])
        external_id = Characteristic(category="External ID", value=miappe_observation_unit["External ID"])
        spatial_distribution = Characteristic(category="Spatial Distribution",
                                              value=miappe_observation_unit["Spatial distribution"])

        return Sample(
            name=miappe_observation_unit['Observation unit ID'],
            characteristics=[unit_type,
                             external_id,
                             spatial_distribution],
            factor_values=FactorValue(value=miappe_observation_unit["Observation Unit factor value"])
        )

    @staticmethod
    def create_sample(miappe_sample: pd.Series) -> dict:
        extract_name = miappe_sample['Sample ID']
        plant_extract = Extract(
            characteristics=[
                Characteristic(category='Plant Structure Development Stage',
                               value=miappe_sample['Plant structure development stage']),
                Characteristic(category='Plant Anatomical Entity', value=miappe_sample['Plant anatomical entity'])
            ]
        )
        external_extract = Extract(
            characteristics=[Characteristic(category="External ID", value=miappe_sample["External ID"])]
        )
        sampling_protocol = Protocol(
            parameters=[
                ParameterValue(category="Sampling Description", value=miappe_sample['Sample description']),
                ParameterValue(category="Sampling Date", value=miappe_sample['Collection date'])
            ]
        )
        return {
            "Extract Name": extract_name,
            "Plant Extract": plant_extract,
            "External ID Extract": external_extract,
            "Sampling Protocol": sampling_protocol
        }

    @staticmethod
    def create_observed_variable(miappe_observed_variable):
        # TODO: add this
        ...

    def add_study(self, miappe_study: pd.Series) -> None:
        new_study = self.create_study(miappe_study)
        self.isa_investigation.studies.append(new_study)
        self.isa_studies[new_study.identifier] = new_study

    def add_person(self, miappe_person: pd.Series) -> None:
        new_person = self.create_person(miappe_person)
        self.isa_people[new_person.id] = new_person

        ids = self.get_study_ids(miappe_person['Study unique ID'])
        for id_ in ids:
            associated_study = self.isa_studies[id_]
            associated_study.contacts.append(new_person)

    def add_data_file(self, miappe_data_file: pd.Series) -> None:
        new_data_file = self.create_data_file(miappe_data_file)

        ids = self.get_study_ids(miappe_data_file['Study unique ID'])
        for id_ in ids:
            associated_study = self.isa_studies[id_]
            associated_study.comments.extend(new_data_file)

    def add_biological_material(self, miappe_biological_material: pd.Series) -> None:
        new_material = self.create_biological_material(miappe_biological_material)

        ids = self.get_study_ids(miappe_biological_material['Study unique ID'])
        for id_ in ids:
            associated_study = self.isa_studies[id_]
            associated_study.sources.append(new_material)

    def add_environment(self, miappe_environment: pd.Series) -> None:
        new_environment_values = self.create_environment(miappe_environment)

        ids = self.get_study_ids(miappe_environment['Study unique ID'])
        for id_ in ids:
            associated_study = self.isa_studies[id_]
            associated_study.get_prot("Growth").add_param(new_environment_values['name'])

            # TODO: figure out what to do with value

    def add_experimental_factor(self, miappe_experimental_factor: pd.Series) -> None:
        new_factor = self.create_experimental_factor(miappe_experimental_factor)

        ids = self.get_study_ids(miappe_experimental_factor['Study unique ID'])
        for id_ in ids:
            associated_study = self.isa_studies[id_]
            associated_study.factors.append(new_factor)

    def add_event(self, miappe_event: pd.Series) -> None:
        new_event = self.create_event(miappe_event)

        ids = self.get_study_ids(miappe_event['Study unique ID'])
        for id_ in ids:
            associated_study = self.isa_studies[id_]
            associated_study.add_protocol(new_event)

    def add_observation_unit(self, miappe_observation_unit: pd.Series) -> None:
        new_sample = self.create_observation_unit(miappe_observation_unit)

        ids = self.get_study_ids(miappe_observation_unit['Study unique ID'])
        for id_ in ids:
            associated_study = self.isa_studies[id_]
            associated_study.samples.append(new_sample)
