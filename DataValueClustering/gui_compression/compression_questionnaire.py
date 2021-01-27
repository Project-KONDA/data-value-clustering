from compression.compression import get_compression_method
from gui_compression.CompressionQuestionnaireResultInput import input_questionnaire_compression
from gui_compression.compression_questions import compression_question_array


def compression_configuration(data, predefined_answers=None):
    answers = input_questionnaire_compression(compression_question_array, data, predefined_answers)
    return get_compression_method(answers), answers

