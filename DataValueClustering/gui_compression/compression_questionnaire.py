from compression.compression import get_compression_method
from gui.QuestionnaireInput import input_questionnaire
from gui.QuestionnaireInputCompression import input_questionnaire_compression
from gui_compression.questions import question_array


def compression_configuration(data, predefined_answers=None):
    answers = input_questionnaire_compression(question_array, data, predefined_answers)
    return get_compression_method(answers), answers

