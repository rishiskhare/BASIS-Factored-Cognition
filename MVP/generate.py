from fvalues import F
import os
from ice.recipe import recipe
import pandas as pd

df = pd.read_csv("prompt_response_validation.tsv", sep='\t')
QUESTIONS = df['Prompt'].tolist()
ANSWERS = df['Response'].tolist()


async def get_answers(): # write to ref and eval csv datasets
    answer = ""
    for i, prompt in enumerate(QUESTIONS):
        # print(prompt)
        if pd.isna(ANSWERS[i]):
            answer = await recipe.agent().complete(prompt=prompt)
            ANSWERS[i] = answer
            # print(answer)
    df['Response'] = ANSWERS
    return # answer #TESTING, remove after confirmation

def write_tsv(prompts, responses, filename):
    """Write prompts and responses to filename"""
    # 1. write df back to OG dataset
    df.to_csv(filename, sep = '\t')
    # 2. make and write questions to eval dataset
    evals = pd.DataFrame({'Prompt': pd.Series(QUESTIONS), 'RESPONSE': pd.Series(ANSWERS)})
    evals.to_csv('safety_evaluations', sep='\t')
    return


recipe.main(get_answers) # FOR TESTING
write_tsv(QUESTIONS, ANSWERS, 'prompt_response_dummy.tsv')