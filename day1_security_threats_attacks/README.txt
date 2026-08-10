
ows, 10 columns
  Includes order, product, value, payment, status, tier, email, phone and support note.

- ai_threat_model.csv
  10 rows, 9 columns
  Includes asset, component, threat, attack path, likelihood, impact, OWASP mapping, control and evidence.

- knowledge_base_demo.csv
  10 rows, 7 columns
  Includes trusted and untrusted ecommerce knowledge documents.

SETUP
1. python -m venv venv
2. Activate the virtual environment.
3. pip install -r requirements.txt
4. Create a .env file:
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-5.5
5. Start Jupyter Notebook.
6. Run notebooks in sequence.
