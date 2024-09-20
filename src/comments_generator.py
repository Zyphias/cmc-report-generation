from openai import OpenAI
client = OpenAI()


def generate_comment(stu_name: str, averages: list[str], feedback: list[str]) -> str:
    """
    Generate a 100 word comment for the student based on the feedback provided.
    - one with general understanding
    - one with work ethic
    - whether they are progressing or not
    """
    # Create a completion
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""
             
                You are the tutor for {stu_name} in a mathematics class.
                You are responsible for generating the comments for {stu_name}'s term report card.
                Their averages in terms of understanding, fluency, problem solving and homework are: {averages[0]}, {averages[1]}, {averages[2]}, {averages[3]} respectively.
                Each week's comments are as follows: {feedback}
                
                Given this information, please generate three paragraphs:
                - one referencing the student's general understanding
                - one referencing the student's work ethic and general homework completion (don't mention specific instances).
                - one referencing the student's progress, or lack thereof.

                The paragraphs should be around 20 words long and should be concise and professional. Please use similar wording to those of the metrics.
                Please ensure there are no contradictions between the paragraphs. e.g. if a student is making progress, do not mention a lack of progress.
                
                The metrics are below. 

                Understanding Metric:
                A - Demonstrates a thorough and comprehensive grasp of mathematical concepts."
                B - Shows a strong understanding with minor errors or gaps in knowledge.
                C - Displays a basic understanding but with some noticeable gaps or misconceptions.
                D - Understands parts of the concepts but lacks overall clarity and consistency.
                E - Shows minimal understanding of the mathematical concepts.
             
                Fluency Metric:
                A - Accurately and efficiently performs routine mathematical procedures consistently.
                B - Performs routine procedures correctly most of the time with minor mistakes.
                C - Completes routine procedures with some accuracy but often makes errors.
                D - Struggles with accuracy and consistency in performing routine procedures.
                E - Rarely performs routine mathematical procedures accurately or efficiently.
             
                Problem Solving Metric:
                A - Effectively applies concepts to solve both routine and non-routine problems accurately.
                B - Successfully solves routine problems and most non-routine problems with minor errors or occasional assistance.
                C - Solves routine problems correctly but struggles with non-routine problems.
                D - Attempts routine problem-solving with limited success and frequently makes errors on non-routine problems.
                E - Struggles significantly with applying concepts to solve both routine and non-routine problems.

                Here are some additional guidelines:
                - It should be in third person
                - Only use the student's first name
                - Do not mention any specific topics
                - Do not use semicolons
                - non-routine is hyphenated. Please ensure that's the case in your response.
                - Only the first dot point should mention the student's name, refer to the student by either 'she' or 'he' in the other dot points
                - Do not use 'keep up the good work' or 'try harder' comments
                - Speak on qualitative aspects of the student's learning and effort, not quantitative data
                - Please refer to assignments as tasks and efforts as effort.
                - Instead of 'making effort' use 'demostrating effort'.
                - Ensure 'problem solving' is two words and not one.
                - Li Qing is a 'he', Parsa is also a 'he', Tanish is a 'he', Anji is a he.
                - Vienna is a 'she'
                - Joy is a 'she'
                - Do not mention school.
                - Do not include more than 1 line break per dot point.
                - Aakriti is a 'she', so is Jewel, so is Shanning
                - Ashwin is a he.
                - For Anders, do not mention he forgets concepts, instead mention need for more problem solving.
                - Ensure there are no contradictions between the dot points.
                Before submitting, please ensure that the feedback is concise and professional and that it makes gramattical and syntactical sense.
            """},
        ]
    )
    feedback = completion.choices[0].message.content

    return feedback

    # return """Gemma demonstrates a solid understanding of key concepts, showing improvement after revising foundational topics.

    # Her work ethic is commendable, as evidenced by her ability to engage with challenging material and apply learned skills effectively.

    # Gemma is making consistent progress in her learning journey, particularly in her application of concepts.
    # """
