
Fetches world news using Python from the NewsData API, summarizes the news with Ollama, and sends the summarized updates to WhatsApp using Twilio

python -m venv venv
python -m pip install --upgrade pip setuptools wheel
venv\Scripts\activate

To install the packages
pip install -r requirements.txt

To run application 
python main.py


pip install twilio
pip install python-dotenv
