from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    try:
        ticker = ticker.upper()
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1d")
        
        if hist.empty:
            return jsonify({"error": f"Ticker {ticker} not found"}), 404
        
        price = hist['Close'].iloc[-1]
        info = stock.info
        div_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
        
        try:
            options_dates = stock.options
            exp1 = options_dates[0] if len(options_dates) > 0 else None
            exp2 = options_dates[1] if len(options_dates) > 1 else None
        except:
            exp1, exp2 = None, None
        
        return jsonify({
            "ticker": ticker,
            "price": round(price, 2),
            "dividend": round(div_yield, 4),
            "exp1": exp1,
            "exp2": exp2,
            "riskFreeRate": 4.0
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

Klick **"Commit new file"**

---

### **Datei 3: `Procfile`**
Klick wieder **"Add file"** → **"Create new file"**

Name: `Procfile` (wichtig: großes P, kein Punkt am Ende!)

Kopiere rein:
```
web: gunicorn app:app
```

Klick **"Commit new file"**

---

## **SCHRITT 4: Render verbinden (3 Min)**

1. Gehe zu **render.com**
2. Klick **"Sign up"** (mit GitHub ist einfachste)
3. GitHub-Login → Authorize Render
4. Nach Login: Klick **"New +"** → **"Web Service"**
5. Klick **"Connect a repository"**
6. Suche dein Repository: `calendar-spread-api`
7. Klick **"Connect"**

---

## **SCHRITT 5: Deployment konfigurieren (2 Min)**

Render fragt dich jetzt einige Sachen. Füll das so aus:

- **Name:** `calendar-spread-api`
- **Runtime:** `Python 3`
- **Build Command:** 
```
  pip install -r requirements.txt
```
- **Start Command:** 
```
  gunicorn app:app
```
- **Region:** `Frankfurt (eu-west-1)` (oder closest to you)
- **Instance Type:** `Free`

Klick **"Deploy Web Service"**

---

## **SCHRITT 6: Warten (2-3 Min)**

Render deployed jetzt deine App. Du siehst einen Log mit:
- Build läuft
- Dependencies werden installiert
- Service startet

Wenn alles grün ist und keine Fehler auftauchen → **SUCCESS!**

---

## **SCHRITT 7: Deine API-URL**

Nach erfolgreichem Deploy siehst du oben eine URL wie:
```
https://calendar-spread-api.onrender.com
```

**Test die API:**
Öffne in neuem Tab:
```
https://calendar-spread-api.onrender.com/api/stock/AAPL
