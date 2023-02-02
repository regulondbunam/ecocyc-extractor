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
        #experiment_gc = experiment_gc.encode('utf-8')
        experiment_gc = f'{experiment_gc}'
        experiment_gc = experiment_gc.replace("GCs_GeneExpression_EXP: ", "")
        experiment_gc = experiment_gc.replace("Growth Condition-chip-Experiment: ", "")

        self._experiment_gc = experiment_gc

    @property
    def control_gc(self):
        return self._control_gc

    @control_gc.setter
    def control_gc(self, control_gc):
        #control_gc = control_gc.encode('utf-8')
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
