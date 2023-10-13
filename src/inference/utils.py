import os
import openai
import hashlib
import numpy as np
import pandas as pd

from openai.embeddings_utils import get_embedding

def load_model(name):
    def model(prompt, **model_kwargs):
        return openai.Completion.create(
            engine=name,
            prompt=prompt,
            **model_kwargs)['choices'][0]['text'].strip()

    return model

def complete(model, prompt, **model_kwargs):
    result = model(prompt, **model_kwargs)
    return result

def get_check_sum(file_path):
    hash_obj = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            hash_obj.update(data)

    return hash_obj.hexdigest()

def load_reference(ref_path):
    try:
        ref_data = pd.read_excel(ref_path, usecols=['REF'])
    except:
        print('Can not find reference data. Set the semantic_search argument alaway is false!!!')
        return None

    check_sum = get_check_sum(ref_path)
    embd_file = os.path.join('/data/embeddings', check_sum+'.csv')
    try:
        ref_data = pd.read_csv(embd_file)
        ref_data['embeddings'] = ref_data['embeddings'].apply(eval).apply(np.array)
        print(f'load embeddings from {embd_file}')
    except:
        print(f'encode reference data to embeddings')
        ref_data['embeddings'] = ref_data['REF'].apply(lambda x: get_embedding(x, engine=os.getenv('OPENAI_ENCODER')))

        ref_data.to_csv(embd_file)
        print(f'save embeddings to {embd_file}')

    return ref_data
