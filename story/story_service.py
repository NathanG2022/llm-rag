import re

from crewai import Agent, Task, Crew, Process

from common.lc_modules import getLlm

# llm = Ollama(base_url='http://localhost:11434', model="llama3")
llm = getLlm()

# Define Agents
analyst = Agent(
    role='Motion Analyst',
    goal='''You will analyze all human motion-related descriptions in the story and extract motion action sequences. Carefully interpret the text to recognize motion-related actions including, gestures, emotions, directions, speeds of the humanoid characters. All other motions of non-human characters can be ignored. You may reword the motion descriptions as long as the main storyline remains intact. Descriptions should focus on a singular character’s motion and should not include multiple character’s actions.''',
    backstory='You are an expert Motion Analyst with extensive experience in breaking down and interpreting human motion sequences. Your knowledge of biomechanics and behavioral psychology allows you to understand the complexities of human motion and how it relates in a 3D space for translation to animation.',
    llm=llm,
    verbose=True,
    allow_delegation=False
)

prompt_writer = Agent(
    role='Prompt Writer',
    goal='''You will analyze the human motion descriptions produced by the Motion Analyst to create textual prompts. Prompts are meant to direct the full body motions and emotions of a singular humanoid character. Prompts can be up to 256 characters. Begin prompts by first describing who singularly is performing the motion. Use "A person" unless the description clearly indicates a specific subject. Prompts should be concise, intuitive, and reflective of the motion. Prompts should be broken down into a maximum of 3 actions in a single motion prompt sequence.''',
    backstory='You are an expert Prompt Writer with a deep understanding of translating detailed human motion analyses into precise and intuitive textual prompts. Your expertise lies in distilling complex descriptions of human motion into clear and actionable prompts that can be used to generate lifelike animations of humanoid characters in a 3D space.',
    llm=llm,
    verbose=True,
    allow_delegation=False
)


def split_text(input_text):
    text_without_asterisks = input_text.replace('*', '')

    lines = text_without_asterisks.split('\n')

    cleaned_lines = [line.strip() for line in lines]

    return cleaned_lines


def get_prompts(story: str) -> [str]:
    # Process post with a crew of agents, ultimately delivering a well formatted dialogue
    task1 = Task(description='Analyze in detail the following story:\n### STORY:\n' + story, agent=analyst,
                 expected_output='A detailed analysis of the story focusing on the animation-related descriptions and identifying the motion actions.')
    task2 = Task(
        description='Create an itemized story focusing on heavy screenplay actions from the story. Do NOT write parentheticals. Leave out wrylies. DO NOT SKIP directional notes.',
        agent=prompt_writer,
        expected_output='A formatted prompt with itemized story focusing on motion actions. NO need for scene division. NO need title, NO need serial number.')

    crew = Crew(
        agents=[analyst, prompt_writer],
        tasks=[task1, task2],
        verbose=2,
        # Crew verbose more will let you know what tasks are being worked on, you can set it to 1 or 2 to different logging levels
        process=Process.sequential
        # Sequential process will have tasks executed one after the other and the outcome of the previous one is passed as extra content into this next.
    )

    result = crew.kickoff()

    # Get rid of directions and actions between brackets, e.g., (smiling)
    result = re.sub(r'\(.*?\)', '', result)

    print('===================== end result from crew ===================================')
    print(result)
    return split_text(result)


if __name__ == "__main__":
    story = '''Title: The Dance of Dreams
  In the heart of a serene forest clearing, a lone character named Liam stands surrounded by towering trees and dappled sunlight. The clearing is their sanctuary, a place where dreams come alive through movement.
  Liam begins by standing still, taking a deep breath, and feeling the energy of the forest. They slowly raise their arms, stretching upwards as if reaching for the sky, then bring them down gracefully, bending at the waist to touch their toes. This stretch sets the stage for a series of fluid, dance-like motions.
  Liam takes a step forward, then twirls gracefully, letting their body follow the momentum. They perform a series of spins and leaps, each movement full of grace and fluidity. With each twirl, Liam's body language conveys joy and freedom. They leap into the air, legs extended, and land softly, transitioning into a series of flowing arm movements that mimic the rustling of leaves.
  As the dance continues, Liam's motions become more expressive. They bend backwards in a dramatic arch, then spring forward, embodying the spirit of the forest. Every movement tells a story, from gentle sways to energetic jumps, all confined within the clearing.
  In the final moments, Liam slows down, their movements becoming more serene. They end with a deep, reverent bow, arms outstretched to the sides, embracing the tranquility of the forest.
  '''
    #     story = '''A young woman timidly walks forward into a dimly lit fighting arena. She looks around quickly at what she assumes to be an empty arena, the sound of past fights still ringing in her ears. She hesitates, shifting her weight from foot to foot, her shoulders tense with apprehension.
    # Taking a deep breath, she steps forward, retracing the steps of those she has avidly followed and admired for so long. Her body flows into a low, graceful spin on a single leg, her other leg extended and sweeping across the floor. Rising from the spin, she pivots sharply to the right, her body twisting with a sudden burst of energy as she lifts her leg high into a powerful roundhouse kick that cuts through the air with precision. Landing softly, she transitions into a series of swift motions: a sidestep to the left with her body crouched low, then a leap into the air, her legs extending in a controlled scissor kick.
    # Suddenly, she freezes and drops to the ground. Was that a noise? She snaps her head looking quickly from side to side. Her posture shifts from confidence to fear. Without a second thought, she turns and sprints toward the edge of the arena, her movements quick and agile. Her feet pound against the ground, her body leaning forward as she races into the shadows, taking a brief last look behind her as she then disappears from sight. The silence of the arena remains, echoing her sudden departure, but ever waiting for the next visit.
    #   '''
    res = get_prompts(story)
    print(res)
