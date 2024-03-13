import time
from threading import Thread
import pandas as pd
from single import call_model

wait_number = 0
types = ['接受', '记忆', '应用', '提问', '阐述', '创造', '支持', '反对', '讨论', '无内容']


def update_column(df, index):
    history = ''
    for i in range(index - 6, index):
        if i < 0:
            continue
        if str(df.loc[i]['Value']) == '':
            continue
        history += str(df.loc[i]['Value']) + ' - Predict: ' + str(df.loc[i]['predict']) + '\n'
    if history == '':
        history = '无上文'
    try:
        text = df.loc[index]['Value']
        print(f'Task {index}:\n{text}\nHistory:\n{history}\n')
        response = call_model(text, history)
        if response == 'ERROR':
            result = 'ORIGIN_ERROR'
        else:
            try:
                type_positions = {type_word: response.rfind(type_word) for type_word in types}
                type_positions = {word: pos for word, pos in type_positions.items() if pos != -1}
                if not type_positions:
                    type_result = '无内容'
                else:
                    type_result = max(type_positions, key=type_positions.get)
                if type_result == '无内容':
                    type_result = '无'
                print('\nFinally Analysis Result:', type_result)

                df.at[index, 'predict'] = type_result
                result = response
                print('\n-------------------------------------\n')
            except Exception as e:
                result = 'PARSE_ERROR'
                print(e)
    except Exception as e:
        result = 'UNKNOWN_ERROR'
        print(e)
    df.at[index, 'info'] = result
    try:
        df.to_excel('./marked/result.xlsx')
    except:
        print('Warning: save error')
    global wait_number
    wait_number -= 1


if __name__ == '__main__':
    num = -1
    print('\n')
    df = pd.read_excel('./middle/output/text_video.xlsx')
    df['predict'] = pd.NA
    df['info'] = pd.NA
    for index, row in df.iterrows():
        if index < 6:
            continue
        if 'Value' in row:
            wait_number += 1
            # Thread(target=update_column, args=(df, index)).start()
            update_column(df, index)
            time.sleep(0.4)
        if 0 <= num <= index + 1:
            break
    while wait_number > 0:
        time.sleep(0.1)
    df.to_excel('./marked/result.xlsx')
    print('\nAll Data Saved.')
