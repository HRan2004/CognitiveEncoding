import time
import openai
from http import HTTPStatus
import httpx
from dashscope import Generation


def call_qwen(user_prompt, system_prompt='你是个语言能力和逻辑理解能力很强的AI助手'):
  messages = [{'role': 'system', 'content': system_prompt},
              {'role': 'user', 'content': user_prompt}]
  # global last_call_time
  # while time.time() - last_call_time < 61:
  #   time.sleep(0.1)
  # last_call_time = time.time()

  try:
    responses = Generation.call(
      'qwen-max',
      messages=messages,
      result_format='message',  # set the result to be "message" format.
      stream=True,
      incremental_output=True  # get streaming output incrementally
    )
    full_content = ''  # with incrementally we need to merge output.
    for response in responses:
      if response.status_code == HTTPStatus.OK:
        content = response.output.choices[0]['message']['content']
        full_content += content
        print(content, end='')
      else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
          response.request_id, response.status_code,
          response.code, response.message
        ))
    if len(full_content) == 0:
      full_content = 'ERROR'
    return full_content
  except Exception as e:
    print(e)
    return 'ERROR'
