# AI Smart Irrigation System

## Run in VS Code (Windows)

Open this folder in VS Code, then open Terminal and run:

```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

## If `python` is not recognized

Use `py` instead:

```powershell
py -m venv venv
venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
py app.py
```

## Project structure

- `app.py` - Flask backend
- `templates/index.html` - input page
- `templates/result.html` - prediction result page
- `static/style.css` - styling
- `irrigation_model.pkl` - trained model
- `irrigation_prediction.csv` - dataset
