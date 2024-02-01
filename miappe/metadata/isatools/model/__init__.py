"""ISA Model 1.0 implementation in Python.

This module implements the ISA Abstract Model 1.0 as Python classes, as
specified in the `ISA Model and Serialization Specifications 1.0`_, and
additional classes to support compatibility between ISA-Tab and ISA-JSON.

Todo:
    * Check consistency with published ISA Model
    * Finish docstringing rest of the module
    * Add constraints on attributes throughout, and test

.. _ISA Model and Serialization Specs 1.0: http://isa-specs.readthedocs.io/

"""
from miappe.metadata.isatools.model.assay import Assay
from miappe.metadata.isatools.model.characteristic import Characteristic
from miappe.metadata.isatools.model.comments import Commentable, Comment
from miappe.metadata.isatools.model.context import set_context
from miappe.metadata.isatools.model.datafile import (
    DataFile,
    RawDataFile,
    DerivedDataFile,
    RawSpectralDataFile,
    DerivedArrayDataFile,
    ArrayDataFile,
    DerivedSpectralDataFile,
    ProteinAssignmentFile,
    PeptideAssignmentFile,
    DerivedArrayDataMatrixFile,
    PostTranslationalModificationAssignmentFile,
    AcquisitionParameterDataFile,
    FreeInductionDecayDataFile
)
from miappe.metadata.isatools.model.factor_value import FactorValue, StudyFactor
from miappe.metadata.isatools.model.investigation import Investigation
from miappe.metadata.isatools.model.logger import log
from miappe.metadata.isatools.model.material import Material, Extract, LabeledExtract
from miappe.metadata.isatools.model.mixins import MetadataMixin, StudyAssayMixin, _build_assay_graph
from miappe.metadata.isatools.model.ontology_annotation import OntologyAnnotation
from miappe.metadata.isatools.model.ontology_source import OntologySource
from miappe.metadata.isatools.model.parameter_value import ParameterValue
from miappe.metadata.isatools.model.person import Person
from miappe.metadata.isatools.model.process import Process
from miappe.metadata.isatools.model.process_sequence import ProcessSequenceNode
from miappe.metadata.isatools.model.protocol import Protocol, load_protocol_types_info
from miappe.metadata.isatools.model.protocol_component import ProtocolComponent
from miappe.metadata.isatools.model.protocol_parameter import ProtocolParameter
from miappe.metadata.isatools.model.publication import Publication
from miappe.metadata.isatools.model.sample import Sample
from miappe.metadata.isatools.model.source import Source
from miappe.metadata.isatools.model.study import Study
from miappe.metadata.isatools.model.logger import log
from miappe.metadata.isatools.model.utils import _build_assay_graph, plink, batch_create_assays, batch_create_materials, _deep_copy
