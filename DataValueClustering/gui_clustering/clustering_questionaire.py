from gui_clustering.ClusteringQuestionnaireInput import input_questionnaire_clustering
from gui_clustering.clustering_questions import question_array


def cluster_suggest():
    predefined_answers = None  # TODO
    answers, cluster_f = input_questionnaire_clustering(question_array, predefined_answers)
    return cluster_f(answers)
