from openai import OpenAI

client = OpenAI(
  api_key="sk-GP24CxnWGtJass1sC98657B71343418780FeE06d7b0a00Bb",
  base_url="https://api.gpts.vin/v1",
)


def call_gpt4(user_prompt, system_prompt='你是个语言能力和逻辑理解能力很强的AI助手'):
  messages = [{'role': 'system', 'content': system_prompt},
              {'role': 'user', 'content': user_prompt}]
  try:
    stream = client.chat.completions.create(
      model="gpt-4-turbo-preview",
      messages=messages,
      stream=True,
      temperature=0.9,
      top_p=0.1,
    )
    text = ''
    for chunk in stream:
      if chunk.choices[0].delta.content is not None:
        content = chunk.choices[0].delta.content
        text += content
        print(content, end="")
    if len(text) > 0:
      return text
  except Exception as e:
    print(e)
  return 'ERROR'

