import re
import operator
import openai
from decouple import config
from flask_restx import abort
from http import HTTPStatus



openai.api_key = config('OPENAI_KEY')







def process_language(text: str) -> int | bool:
    """process arithemetic operation from input sentence

    Args:
        text (str): input sentence

    Returns:
        int | bool
    """
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt=f"{text}",
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    result: str = response['choices'][0]['text']
    result = result.replace('\n', '').strip()
    print(result, type(result))
    if re.search(r'\d+', result):
        answer = int(re.findall(r'\d+', result)[-1])
        print(f'FIRST RRESULT: {answer}')
        return answer
        
    return False





operators = {
    "addition": operator.add,
    "multiplication": operator.mul,
    "subtraction": operator.sub
}



def process_operation(
    data: dict[str, str | int]
    ) -> dict[str, str | int]:
    """return result of arithimetic operation from endpoint

    Args:
        data (dict[str, str  |  int]): request data

    Returns:
        dict[str, str | int]
    """
    operation = data.get('operation_type')
    x = data.get('x')
    y = data.get('y')
    if operation in operators:
        op = operators[operation]
        try:
            result = op(x, y)
        except TypeError:
            return abort(
                code=HTTPStatus.BAD_REQUEST, 
                message="provide valid input operands"
                )
    else:
        result = process_language(operation)
    if not result:
        return abort(
            code=HTTPStatus.BAD_REQUEST,
            message="failed to calculate result"
        )
    return {
        "slackUsername": "anonnoone", 
        "operation_type" : operation or "curvaceous", 
        "result": result
    }, HTTPStatus.OK
        


