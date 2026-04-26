import time
import json
import io
from conf import gen_model
from flask_restful import Resource
from flask import request
import PyPDF2
import docx

class Quiz_Generator:
    def __init__(self):
        # {num_questions} is injected dynamically
        self.template = """
        Read the whole document carefully and generate exactly {num_questions} multiple-choice questions.
        Each question must have exactly 4 options, out of which exactly 1 is correct.

        Here is the document content:
        {document_data}

        Return a JSON object with exactly {num_questions} questions in this format:
        {{
            "Q1": {{
                "ques": "Question text here?",
                "opt1": "First option",
                "opt2": "Second option",
                "opt3": "Third option",
                "opt4": "Fourth option",
                "ans": "opt2"
            }},
            "Q2": {{ ... }},
            ...
            "Q{num_questions}": {{ ... }}
        }}

        Rules:
        - The "ans" key must contain the KEY of the correct option: "opt1", "opt2", "opt3", or "opt4"
        - Distribute correct answers randomly across all 4 options — do not always put the answer in opt1
        - Generate exactly {num_questions} questions, no more, no less
        - Base all questions strictly on the document content
        - Mix easy, medium, and hard difficulty questions
        - Return ONLY raw JSON. No markdown, no code fences, no explanation.
        - Start your response with '{{' and end with '}}'
        """

    def extract_text(self, file, filename: str) -> str:
        ext = filename.rsplit('.', 1)[-1].lower()
        text = ""

        if ext == "txt":
            text = file.read().decode('utf-8')
        elif ext == "pdf":
            reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            for page in reader.pages:
                text += page.extract_text() or ""
        elif ext == "docx":
            doc = docx.Document(io.BytesIO(file.read()))
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError(f"Unsupported file type: .{ext}. Please upload PDF, DOCX, or TXT.")

        text = text.strip()
        if not text:
            raise ValueError("No text could be extracted from this file.")

        # Truncate to 12000 chars to stay within Gemini token limits safely
        return text[:12000]

    def generate_questions(self, document_text: str, num_questions: int = 10) -> dict:
        prompt = self.template.format(
            document_data=document_text,
            num_questions=num_questions
        )

        response = gen_model.generate_content(prompt)
        result = response.text.strip()

        # Safety strip
        result = result.replace("```json", "").replace("```", "").strip()

        # Robustly extract only the JSON object
        start_index = result.find("{")
        end_index = result.rfind("}")
        if start_index == -1 or end_index == -1:
            raise ValueError("Gemini did not return valid JSON. Please try again.")

        result = result[start_index:end_index + 1]
        json_result = json.loads(result)
        return json_result

quiz_obj = Quiz_Generator()

class GenerateQuizAPI(Resource):
    def post(self):
        if 'file' not in request.files:
            return {"status": "error", "message": "No file provided in the request"}, 400

        file = request.files['file']
        if not file or file.filename == "":
            return {"status": "error", "message": "No file selected"}, 400

        # Read and validate num_questions
        try:
            num_questions = int(request.form.get('num_questions', 10))
        except (ValueError, TypeError):
            num_questions = 10

        if num_questions not in [10, 15, 20]:
            num_questions = 10

        allowed_extensions = {'pdf', 'docx', 'txt'}
        filename = file.filename
        if '.' not in filename or filename.rsplit('.', 1)[-1].lower() not in allowed_extensions:
            return {
                "status": "error",
                "message": "Only PDF, DOCX, and TXT files are supported"
            }, 400

        try:
            text = quiz_obj.extract_text(file, filename)
            json_data = quiz_obj.generate_questions(
                document_text=text,
                num_questions=num_questions
            )

            return {
                "status": "success",
                "message": f"Successfully generated {num_questions} questions!",
                "num_questions": num_questions,
                "content": json_data,
            }, 200

        except ValueError as e:
            return {"status": "error", "message": str(e)}, 400
        except Exception as e:
            return {
                "status": "exception",
                "message": f"Error generating quiz: {str(e)}"
            }, 500
