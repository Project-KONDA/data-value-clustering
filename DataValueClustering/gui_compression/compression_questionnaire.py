from compression.compression import get_compression_method, question_array
from gui.QuestionnaireInput import QuestionnaireInput, input_questionnaire


def automatic():
    answers = input_questionnaire("Compression Configuration", question_array)
    return get_compression_method(answers)