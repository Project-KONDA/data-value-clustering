from compression.compression import get_compression_method
from gui.QuestionnaireInput import input_questionnaire
from gui.QuestionnaireInputCompression import input_questionnaire_compression
from gui_compression.questions import question_array


def automatic():
    data = None  # TODO
    predefined_answers = None  # TODO
    answers = input_questionnaire_compression(question_array, data, predefined_answers)
    return get_compression_method(answers), answers

