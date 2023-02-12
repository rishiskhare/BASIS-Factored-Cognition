from fvalues import F

from ice.recipe import recipe

all_answers = []

DEFAULT_CONTEXT = "We're running a hackathon on 9/9/2022 to decompose complex reasoning tasks into subtasks that are easier to automate & evaluate with language models. Our team is currently breaking down reasoning about the quality of evidence in randomized controlled trials into smaller tasks e.g. placebo, intervention adherence rate, blinding procedure, etc."

DEFAULT_QUESTION = "What should we make sure we do to make sure the hackathon goes well?"


def make_qa_prompt(context: str, question: str) -> str:
    return F(
        f"""
Background text: "{context}"

Answer the following question about the background text above:

Question: "{question}"
Answer: "Let's think step by step.
"""
    ).strip()


async def answer(
    context: str = DEFAULT_CONTEXT, question: str = DEFAULT_QUESTION
) -> str:
    prompt = make_qa_prompt(context, question)
    answer = await recipe.agent().complete(prompt=prompt, stop='"')
    for i in range(0,10):
        context1 = context + "You answered: " + answer
        question = "How can you improve on this answer?"
        prompt = make_qa_prompt(context1, question)
        answer = await recipe.agent().complete(prompt=prompt, stop='"')
        all_answers.append(answer)
    return answer


recipe.main(answer)
print(all_answers)
