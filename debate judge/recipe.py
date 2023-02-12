from ice.agents.base import Agent
from ice.recipe import recipe
from ice.recipes.primer.debate.prompt import *

#judge = recipe.agent()
judge_context = ""

async def turn(debate: Debate, agent: Agent, agent_name: Name, turns_left: int):
    prompt = render_debate_prompt(agent_name, debate, turns_left)
    answer = await agent.complete(prompt=prompt, stop="\n")
    return (agent_name, answer.strip('" '))

async def make_judge_prompt(context) -> str:
    question = "Did Alice or Bob win the debate?"
    return F(
        f"""
Background text: "{context}"

Answer the following question about the background text above:

Question: "{question}"
Answer: "Let's think step by step.
"""
    ).strip()


async def debate(question: str = "Should we legalize all drugs?"):
    agents = [recipe.agent(), recipe.agent()]
    agent_names = ["Alice", "Bob"]
    debate = initialize_debate(question)
    turns_left = 8
    while turns_left > 0:
        for agent, agent_name in zip(agents, agent_names):
            response = await turn(debate, agent, agent_name, turns_left)
            debate.append(response)
            judge_context += response
            turns_left -= 1
    #return render_debate(debate)
    return judge_decide()

async def judge_decide():
    prompt = make_judge_prompt(judge_context)
    answer = await recipe.agent().complete(prompt=prompt, stop='"')
    return answer

recipe.main(debate)
#recipe.main(judge_decide)