from .base import Base


class Evidence(Base):

    def __init__(self, **kwargs):
        super(Evidence, self).__init__(**kwargs)
        self.code = kwargs.get("code", None)
        self.pertains_to = kwargs.get("pertains_to", None)

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, name=None):
        evidence_code_to_return = None
        if name is not None:
            tokens_to_exclude = ['of', 'in', 'by', 'on', 'from', 'to', 'is', 'a',
                                 'that']
            # Replacing "-" with an empty space from the name, Since there are evidences that may seem
            # with a repeated
            # i.e: "CHIP-chip evidence" AND "CHIP-exo evidence", would end up with CE and CE as evidence code
            # with this change now the code will be CCE and CEE
            evidence_code_list = name.replace("-", " ")
            # we create a list, each word of the evidence name will be an element
            # of the list
            evidence_code_list = evidence_code_list.split(" ")
            evidence_code_to_return = ""
            # Looping through tokensToExclude's elements to remove them from the
            # evidenceCodeList
            for token in tokens_to_exclude:
                # Removing the element of tokensToExclude that is inside the
                # evidenceCodeList
                while token in evidence_code_list:
                    evidence_code_list.remove(token)
            # We take the first character of each element from the
            # evidenceCodeList to
            # create the evidence code
            for evidence_code in evidence_code_list:
                if evidence_code != "":
                    evidence_code_to_return = evidence_code_to_return + evidence_code[0]
            self._code = evidence_code_to_return.upper()
        else:
            self.code = None

    @property
    def pertains_to(self):
        return self._pertains_to

    @pertains_to.setter
    def pertains_to(self, classes=None):
        if classes is not None:
            pertains_to = []
            for class_id in classes:
                pertains_to.append(class_id.replace("|", ""))
            self._pertains_to = pertains_to
        else:
            self._pertains_to = None
