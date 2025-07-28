import pytesseract
from pdf2image import convert_from_path
from .models import Question
import re




def extract_questions_from_pdf(exam):
    print("PDF path:", exam.exam_paper.path)
    pages = convert_from_path(exam.exam_paper.path)
    print("Total pages converted:", len(pages))

    question_number = 1
    for page in pages:
        text = pytesseract.image_to_string(page)
        print("OCR TEXT:", text[:1000])  # Print first 1000 characters
        questions = split_questions(text)
        print("Questions Found:", questions)


        for q in questions:
            if not q.strip():
                continue
            Question.objects.create(
                exam=exam,
                question_number=question_number,
                question_text=q.strip()
            )
            question_number += 1


def split_questions(text):
    # Pattern for "Question One", "Question Two", ..., including "Question One a"
    pattern = re.compile(r'(Question\s+(?:[A-Z][a-z]+\s?[a-z]?)\s*)', re.IGNORECASE)

    parts = pattern.split(text)
    questions = []

    for i in range(1, len(parts), 2):
        question_title = parts[i].strip()
        question_body = parts[i+1].strip() if i+1 < len(parts) else ""
        full_question = f"{question_title} {question_body}".strip()
        questions.append(full_question)

    return questions
