# 🏁 F1 Financial Regulations Q&A - AI Powered Document Search

This project leverages AWS services — S3, Kendra, and Bedrock — to create an intelligent document search system that allows users to query a PDF of the Formula 1 Financial Regulations and receive context-aware, natural language answers.

---

## ⚙️ Architecture
![formula1-AI drawio](https://github.com/user-attachments/assets/5df64582-75f8-42ae-96b4-29e3ba68e508)


User -> Kendra -> Retrieves context from indexed S3 documents -> Bedrock(Tita) -> Generates Respone

### 🔁 Workflow

1. **PDF Document** is uploaded to an S3 bucket.
2. **Textract** (optional step, not included) extracts text, indexes it and saves to S3 for Kendra to query if the PDF is image-based.
3. **Kendra** indexes the text stored in S3.
4. **Python script** sends user queries to Kendra and retrieves the most relevant passages.
5. **Bedrock Titan model** is prompted to generate a human-like answer with that context.

---

## 🧰 Technologies Used

- **AWS Textract** – OCR for PDFs (Optional)
- **Amazon S3** – Storage of documents and extracted text
- **Amazon Kendra** – Enterprise search with natural language support
- **Amazon Bedrock** – Titan G1 Express for LLM-based question answering
- **Python (boto3)** – Orchestration of the entire pipeline

---

## 🧪 Setup Instructions

1. Upload your PDF to an S3 bucket.
2. (Optional) Run Textract to extract text from scanned PDFS and save the output to S3.
3. Create and configure a Kendra index with S3 as a data source.
4. Make sure Kendra and Bedrock roles have proper permissions.
5. Install requirements:

```bash
pip install boto3

python3 main.py
