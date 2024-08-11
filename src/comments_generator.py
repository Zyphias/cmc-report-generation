from openai import OpenAI
client = OpenAI()


def generate_comment(stu_name: str, averages: list[str], feedback: list[str]) -> str:
    # """
    # Generate a 100 word comment for the student based on the feedback provided.
    # """
    # # Create a completion
    # completion = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": f"""You are a tutor's assistant.
    #             Given each week's feedback for the student and their averages,
    #             generate a 100 word comment for the student's end of term feedback.

    #             It should not mention the student's last name and should not contain quantitative data.
    #             Instead, it should focus on the qualitative aspects of the student's learning and aspect.
    #             Comment on their understanding, fluency and problem solving as a whole.

    #             It should sound like a comment a teacher would write on a report card.
    #             Please address it as third person and be professional.

    #             Please omit any 'keep up the good work' or 'try harder' comments.

    #             Weekly Feedback: {feedback}
    #             Student Name: {stu_name}
    #             Student Averages (Understanding, Fluency, Problem Solving): {averages}

    #          """},
    #     ]
    # )
    # return completion.choices[0].message.content

    return """Kaylie has demonstrated a solid understanding of the material throughout the term,
    consistently grasping key concepts and applying them effectively. Her fluency in
    expressing ideas has become more refined, allowing her to articulate her thoughts
    clearly during discussions. In problem-solving tasks, Kaylie has shown an ability to
    approach challenges methodically, utilizing critical thinking skills to explore multiple
    strategies. This adaptability has enriched her learning experience and contributed
    positively to her growth. Overall, Kaylie has made commendable progress, and her
    engagement in the learning process reflects a dedication that will serve her well in the
    future."""
