from gui_general.ClusteringQuestionnaireResultInput import input_questionnaire_clustering
from gui_clustering.clustering_questions import clustering_question_array


def cluster_suggest():
    predefined_answers = None  # TODO
    answers, cluster_f = input_questionnaire_clustering(clustering_question_array, predefined_answers)
    return cluster_f(answers)  # TODO: call directly or return function to main?
