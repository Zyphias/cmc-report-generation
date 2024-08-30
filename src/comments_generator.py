from openai import OpenAI
client = OpenAI()


def generate_comment(stu_name: str, averages: list[str], feedback: list[str]) -> str:
    """
    Generate a 100 word comment for the student based on the feedback provided.
    ! Three dot points only.
    - one with general understanding
    - one with work ethic
    - whether they are progressing or not
    """
    # Create a completion
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""
             
             
                You are responsible for generating the comments for {stu_name}'s report card.
                Their averages in terms of understanding, fluency, and problem solving are {averages[0]}, {averages[1]}, and {averages[2]} respectively.
                Each week's comments are as follows: {feedback}
                
                Given this information, please generate three dot points:
                - one referencing the student's general understanding
                - one referencing the student's work ethic
                - one referencing the student's progress, or lack thereof.

                The dot points should be around 20 words long and should be concise and professional.
                
                Here are some additional guidelines:
                - It should be in third person
                - Only use the student's first name
                - Do not mention any specific topics
                - Do not use semicolons
                - Only the first dot point should mention the student's name, refer to the student by either 'she' or 'he' in the other dot points
                - Do not use 'keep up the good work' or 'try harder' comments
                - Speak on qualitative aspects of the student's learning and effort, not quantitative data
                - Please refer to assignments as tasks and efforts as effort.
                - Instead of 'making effort' use 'demostrating effort'.
                - Instead of 'problemsolving', use 'problem solving'.
                - Li Qing is a 'he', Parsa is also a 'he'
                - Do not mention school.
                Before submitting, please ensure that the feedback is concise and professional and that it makes gramattical and syntactical sense.
            """},
        ]
    )
    feedback = completion.choices[0].message.content
    # Remove the dashes
    feedback = feedback.replace("-", "")
    # Add new line after each full stop
    feedback = feedback.replace(". ", ".\n")
    # print(feedback)
    return feedback

    # return """Gemma demonstrates a solid understanding of key concepts, showing improvement after revising foundational topics.

    # Her work ethic is commendable, as evidenced by her ability to engage with challenging material and apply learned skills effectively.

    # Gemma is making consistent progress in her learning journey, particularly in her application of concepts.
    # """
