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
