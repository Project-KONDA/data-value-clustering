from compression.compression import get_compression_method
from gui_clustering.clustering_questions import question_array
from gui_compression.CompressionQuestionnaireInput import input_questionnaire_compression


def automatic():
    data = None  # TODO
    predefined_answers = None
    answers = input_questionnaire_compression(question_array, data, predefined_answers)
    return get_compression_method(answers), answers