from compression.compression import get_compression_method
from gui.QuestionnaireInput import input_questionnaire
from gui_compression.questions import question_array


def automatic():
    answers = input_questionnaire("Compression Configuration", question_array)
    return get_compression_method(answers), answers

