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
            {"role": "system", "content": f"""You are a tutor's assistant.
                Given each week's comments for the student and their averages,
                generate three dot points. Do not include the actual dot points.

                - one with general understanding
                - one with work ethic
                - whether they are progressing or not. If they are not, be clear about it.

                It should not mention the student's last name and should not contain quantitative data.
                Instead, it should focus on the qualitative aspects of the student's learning and aspect.
                Do not talk about any specific topics.

                It should sound like a comment a teacher would write on a report card.
                Please address it as third person and be professional.

                Please omit any 'keep up the good work' or 'try harder' comments.

                Here is some data to assist:
                Weekly Feedback: {feedback}
                Student Name: {stu_name}
                Student Averages (Understanding, Fluency, Problem Solving): {averages}

                The dot points need to be short and precise.
                Please refer to assignments as tasks and efforts as effort.
                Do not use semicolons, instead use commas in their place.
                Instead of 'making effort' use 'demostrating effort'.

            """},
        ]
    )
    feedback = completion.choices[0].message.content
    # Remove the dashes
    feedback = feedback.replace("-", "")
    # Add new line after each full stop
    feedback = feedback.replace(". ", ".\n")
    print(feedback)
    return feedback

    # return """Gemma demonstrates a solid understanding of key concepts, showing improvement after revising foundational topics.

    # Her work ethic is commendable, as evidenced by her ability to engage with challenging material and apply learned skills effectively.

    # Gemma is making consistent progress in her learning journey, particularly in her application of concepts.
    # """
