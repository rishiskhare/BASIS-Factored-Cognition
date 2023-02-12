from fvalues import F

from ice.recipe import recipe


DEFAULT_CONTEXT = "I'm making a sandwich on 9/9/2022."

DEFAULT_QUESTION = "What is happening on 9/9/2022?"


def make_qa_prompt(context: str, question: str) -> str:
    return F(
        f"""
Background text: "{context}"

Answer the following question about the background text above:

Question: "{question}"
Answer: "Let's think step by step.
"""
    ).strip()

def make_improvement_prompt(context: str, answer: str, question: str) -> str:
    return F(
        f"""
Background text: "{context}"
Question: "{question}"
Here is an answer to the above question and above background text.
Answer: "{answer}"

How would we improve the answer?

Relevant questions: "
"""
    ).strip()


async def answer(
    context: str = DEFAULT_CONTEXT, question: str = DEFAULT_QUESTION
) -> str:
    prompt = make_qa_prompt(context, question)
    answer = await recipe.agent().complete(prompt=prompt, stop='"')
    improvement_prompt = make_improvement_prompt(context, answer, question)
    improved_answer = await recipe.agent().complete(prompt=improvement_prompt, stop='"')
    return improved_answer


recipe.main(answer)