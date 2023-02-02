import re


class McoTmp(object):
    pattern = "(GCs_GeneExpression_EXP:.+)\s*(GCs_GeneExpression_CONTROL:.+)\s*(<a href.*<\/a>)*"
    pattern_2 = r"(Growth Condition-chip-Experiment:.+)\s*(Growth Conditions_GeneExpression_CONTROL:.+)\s*(<a href.*<\/a>)*"
    citations_pattern = re.compile("(\[[0-9]+\])")
    ri_types = {
        "Gene": "ri-tf-gene",
        "Transcription-Unit": "ri-tf-tu",
        "Promoter": "ri-tf-promoter",
        "ppgpp": "ppGpp-interaction"
    }

    def __init__(self, regulondb_id, ri_object, object_type, pt_conn):
        self.regulondb_id = regulondb_id
        self.ri_object = ri_object
        self.comment = ri_object["comment"]
        self.object_type = object_type
        self.pt_conn = pt_conn
        self.growth_conditions = ri_object["growth_conditions"]

    def get_citations(self, growth_condition, gc_evidences, gc_pmids):
        pmids_found = re.findall(McoTmp.citations_pattern, growth_condition)
        pmids_found = list(set(pmids_found))
        gc_evidences.extend([])
        gc_pmids.extend(pmids_found)

    def get_growth_condition_from_comment(self):
        if not self.comment:
            return []

        growth_conditions = re.match(McoTmp.pattern, self.comment)

        if growth_conditions is None:
            growth_conditions = re.match(McoTmp.pattern_2, self.comment)
        if growth_conditions is None:
            return []

        gc_evidences = []
        gc_pmids = []

        self.get_citations(growth_conditions.group(1), gc_evidences, gc_pmids)
        self.get_citations(growth_conditions.group(2), gc_evidences, gc_pmids)

        experiment_gc = growth_conditions.group(1)
        control_gc = growth_conditions.group(2)

        growth_condition = self.GrowthCondition(experiment_gc, control_gc, gc_evidences, gc_pmids)

        return growth_condition

    def transform_growth_conditions(self, growth_conditions):
        transformed_gc = []
        if not growth_conditions:
            return None
        for growth_condition in growth_conditions:
            if "control" not in growth_condition.lower():
                continue
            growth_conditions = growth_condition.split('CONTROL')
            gc_evidences = []
            gc_pmids = []

            experiment_gc = growth_conditions[0]
            control_gc = growth_conditions[1]

            self.get_citations(experiment_gc, gc_evidences, gc_pmids)
            self.get_citations(control_gc, gc_evidences, gc_pmids)

            growth_condition = self.GrowthCondition(experiment_gc, control_gc,
                                                    gc_evidences, gc_pmids)
            transformed_gc.append(growth_condition)
        return transformed_gc

    @property
    def growth_conditions(self):
        return self._growth_conditions

    @growth_conditions.setter
    def growth_conditions(self, growth_conditions):
        self._growth_conditions = []

        growth_condition = self.get_growth_condition_from_comment()
        growth_conditions = self.transform_growth_conditions(growth_conditions)

        if growth_condition:
            self._growth_conditions.append(growth_condition)
        if growth_conditions:
            self._growth_conditions.extend(growth_conditions)

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        if isinstance(comment, list):
            comment = ", ".join(comment)

        if not comment:
            comment = None

        self._comment = comment

    def __call__(self, *args, **kwargs):
        gcs = []
        for growth_condition in self.growth_conditions:
            mco_tmp = {
                "object_id": self.regulondb_id,
                "object_type": self.object_type,
                "control": growth_condition.control_gc,
                "experiment": growth_condition.experiment_gc,
                "evidences_list": growth_condition.evidences,
                "pmid_list": growth_condition.pmids
            }
            gcs.append(mco_tmp.copy())
        return gcs

    class GrowthCondition(object):

        def __init__(self, experiment_gc, control_gc, evidences, pmids):
            self.experiment_gc = experiment_gc
            self.control_gc = control_gc
            self.evidences = evidences
            self.pmids = pmids

        @property
        def experiment_gc(self):
            return self._experiment_gc

        @experiment_gc.setter
        def experiment_gc(self, experiment_gc):
            experiment_gc = experiment_gc.encode('utf-8')
            experiment_gc = f'{experiment_gc}'
            experiment_gc = experiment_gc.replace("GCs_GeneExpression_EXP: ", "")
            experiment_gc = experiment_gc.replace("Growth Condition-chip-Experiment: ", "")

            self._experiment_gc = experiment_gc

        @property
        def control_gc(self):
            return self._control_gc

        @control_gc.setter
        def control_gc(self, control_gc):
            control_gc = control_gc.encode('utf-8')
            control_gc = f'{control_gc}'
            control_gc = control_gc.replace("GCs_GeneExpression_CONTROL: ", "")
            control_gc = control_gc.replace("Growth Conditions_GeneExpression_CONTROL: ", "")
            control_gc = control_gc.lstrip("2")
            control_gc = control_gc.lstrip(":")
            control_gc = control_gc.lstrip()
            self._control_gc = control_gc

        @property
        def evidences(self):
            return self._evidences

        @evidences.setter
        def evidences(self, evidences):
            evidences = list(set(evidences))
            self._evidences = ", ".join(evidences)

        @property
        def pmids(self):
            return self._pmids

        @pmids.setter
        def pmids(self, pmids):
            pmids = list(set(pmids))
            self._pmids = ", ".join(pmids).replace("[", "").replace("]", "")
