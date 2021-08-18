import pythoncyc
from ecocyc.utils.pathway_tools.connection import Connection
from ecocyc.utils import utils


class Base(object):

    pt_connection = Connection()

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.bnumber = kwargs.get("accession_1", None)
        self.comment = kwargs.get("comment", None)
        self.citations = kwargs.get("citations", None)
        self.db_links = kwargs.get("dblinks", None)
        self.internal_comment = kwargs.get("internal_comment", None)
        self.interrupted = kwargs.get("interrupted", None)
        self.left_end_position = kwargs.get("lend", None)
        self._name = kwargs.get("name", None)
        self._offset = kwargs.get("offset", None)
        self.organism = kwargs.get("organism", None)
        self.right_end_position = kwargs.get("rend", None)
        self.strand = kwargs.get("strand", None)
        self._sequence = None
        self._synonyms = kwargs.get("synonyms", None)

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = self.get_comment(comment)
        if self._comment is not None:
            utils.add_pmids_to_extraction_from(self._comment)

    @property
    def internal_comment(self):
        return self._internal_comment

    @internal_comment.setter
    def internal_comment(self, internal_comment):
        self._internal_comment = self.get_comment(internal_comment)
        if self._internal_comment is None:
            self._internal_comment = ""
        self._internal_comment = self._internal_comment + "; Source: EcoCyc"

    @property
    def citations(self):
        return self._citations

    @citations.setter
    def citations(self, citations):
        citations = utils.get_citations(citations)
        if not citations:
            citations = None
        self._citations = citations

    @property
    def db_links(self):
        return self._db_links

    @db_links.setter
    def db_links(self, external_cross_references):
        self._db_links = []
        try:
            self._db_links.extend(utils.get_external_cross_references(external_cross_references))
        except TypeError:
            pass

        ecocyc_reference = {
            "externalCrossReferences_id": "|ECOCYC|",
            "objectId": self.id.replace("|", ""),
        }

        if ecocyc_reference not in self._db_links:
            self._db_links.append(ecocyc_reference.copy())

        if self.bnumber:
            bnumber_reference = {
                "externalCrossReferences_id": "|REFSEQ|",
                "objectId": self.bnumber,
            }
            self._db_links.append(bnumber_reference.copy())

    @property
    def name(self):
        return self._name

    @property
    def sequence(self):
        if self._sequence is None:
            self._sequence = self.get_sequence(self.left_end_position, self.right_end_position, self.strand, self._offset)
        return self._sequence

    @property
    def strand(self):
        return self._strand

    @strand.setter
    def strand(self, strand=None):
        if strand is None:
            try:
                strand = Base.pt_connection.get_transcription_direction(self.id)
            except pythoncyc.PTools.PToolsError:
                strand = None
        self._strand = self.get_strand(strand)

    @property
    def synonyms(self):
        return self._synonyms

    @staticmethod
    def get_comment(comment):
        try:
            # We try to convert the comment into a str
            # Since there are times where the comment is of type list
            comment = "".join(comment)
        except TypeError:
            # We explicitly pass this error silently
            comment = None
        return comment

    @staticmethod
    def get_strand(strand):
        if strand is not None:
            if strand == -1 or strand == "-":
                strand = "reverse"
            elif strand == 1 or strand == "+":
                strand = "forward"
        return strand

    @staticmethod
    def get_sequence(left_end_position, right_end_position, strand=None, offset=None):
        sequence = None
        if left_end_position and right_end_position:
            # if we have an offset value then we proceed in a different form
            if offset is not None:
                # We add the offset to the positions
                lend = left_end_position - offset
                rend = right_end_position + offset
                # with the positions values modified by the offset we get the
                # sequence
                sequence = Base.pt_connection.get_sequence(lend, rend, "X")
                sequence = sequence[:offset].lower() + sequence[offset:]
                sequence = sequence[: len(sequence) - offset] + sequence[-offset:].lower()
            else:
                sequence = Base.pt_connection.get_sequence(left_end_position, right_end_position, "X")
            if strand == "reverse" and sequence is not None:
                sequence = Base.pt_connection.get_reverse_complement(sequence)
        return sequence

    @staticmethod
    def get_only_properties_with_values(properties):
        properties = {key: value for key, value in properties.items() if value}
        return properties
