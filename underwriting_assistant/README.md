##### **GenAI Underwriting Assistant**

A rule-book driven GenAI underwriting assistant that helps insurance underwriters assess risk by interpreting applicant data, claims history, and external reports against a formal underwriting policy.



###### Key Features

External underwriting rule book (JSON)

Interprets unstructured insurance data

Identifies policy compliance \& risk indicators

Derives an explainable risk score

Generates consistent underwriting recommendations

Built with LangChain + Azure OpenAI



###### Architecture


Flask UI → GenAI Agent → Underwriting Rule Book → Azure OpenAI



###### Setup \& Run


pip install -r requirements.txt
python app.py



###### Open:-


http://127.0.0.1:5000/



###### Output Example



Policy compliance status

Identified risks \& triggered rules

Rule-derived risk score (Low / Medium / High)

Underwriting recommendation

