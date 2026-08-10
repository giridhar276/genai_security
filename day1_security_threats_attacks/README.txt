GENAI SECURITY - HALF DAY 1 ENHANCED NOTEBOOK PACK
====================================================

DESIGN PRINCIPLES
- Simple Python code
- More small, explainable steps
- Realistic synthetic ecommerce CSV files
- Markdown explanation before major code sections
- ASCII architecture diagrams at the top of every notebook
- pip install command in a commented code cell near the top
- OpenAI model configurable through .env
- Evidence-oriented Attack -> Defend -> Retest flow

MAIN NOTEBOOKS
1. 01_vulnerable_ecommerce_chatbot.ipynb
2. 02_prompt_injection_jailbreak_testing.ipynb
3. 03_sensitive_information_disclosure.ipynb
4. 04_ai_threat_modelling_risk_scoring.ipynb
5. 05_attack_defend_retest_basic_security.ipynb

OPTIONAL PREVIEW
6. 06_optional_indirect_prompt_injection_preview.ipynb

REALISTIC SYNTHETIC CSV FILES
- prompt_attack_dataset.csv
  15 rows, 10 columns
  Includes customer tier, channel, issue type, attack type, risk and business impact.

- synthetic_customer_data.csv
  10 rows, 10 columns
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

IMPORTANT
- All customer records are synthetic.
- Security attack prompts are controlled training examples.
- The local prompt detector in Notebook 5 is intentionally simple and demonstrates limitations.
- It is not presented as a production-grade prompt-injection solution.
