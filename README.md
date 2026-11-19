# ☕ Coffee Shop - AI Barista

A Coffee Shop AI Agent powered by OpenRouter. Interact with a friendly AI barista through a clean web interface to browse menu items, get personalized recommendations, and place orders with a shopping cart.

## Features

- **AI-Powered Recommendations** - Conversational barista understands natural language queries
- **Smart Menu Search** - Find drinks and pastries by preferences, dietary restrictions, and tags
- **Shopping Cart** - Add items, adjust quantities, and calculate totals
- **Order History** - Track completed orders in local JSON file
- **Allergen & Dietary Filtering** - Safe recommendations for dietary restrictions
- **Clean UI** - Streamlit-based web interface with coffee-themed design


### Component Overview

| Component | File | Responsibility |
|-----------|------|----------------|
| UI Layer | `app.py` | Streamlit web interface, session state |
| AI Agent | `agent.py` | OpenRouter API calls, response validation |
| Menu Engine | `menu_search.py` | Filtering by tags, allergens, category |
| Cart Manager | `cart_manager.py` | Add/remove items, quantity, totals |
| Config | `config.py` | Env vars, API key loading |
| Menu Data | `data/menu.json` | 8-item coffee shop menu |
| Orders | `data/orders.json` | Persisted order history |

---

## AI Model Configuration

This project uses **OpenRouter** as the AI gateway, which means you are not locked into any single model. You can switch the model at any time by editing `agent.py:92`:

```python
response = self.client.chat.completions.create(
    model="nvidia/nemotron-3.5-lightning:free",  # Change this to any OpenRouter model
    ...
)
```

Browse all available models at **https://openrouter.ai/models** and paste the model ID. Free models are marked with `:free`.

**Example models you can use:**

| Model ID | Notes |
|----------|-------|
| `nvidia/nemotron-3.5-lightning:free` | Current default, free |
| `google/gemma-3-4b-it:free` | Free, fast |
| `meta-llama/llama-3.1-8b-instruct:free` | Free, capable |
| `mistralai/mistral-7b-instruct:free` | Free, lightweight |
| `openai/gpt-4o-mini` | Paid, high quality |
| `anthropic/claude-3-haiku` | Paid, reliable |

No other code changes are needed — just update the model string and restart the app.

---

## Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Sign up here](https://openrouter.ai))

## Setup Instructions

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**
   ```bash
   # Windows PowerShell:
   Copy-Item .env.example .env
   ```
   
   Edit `.env` and add your OpenRouter API key:
   ```
   OPENAI_API_KEY=sk-or-your-openrouter-key-here
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

---

## Usage Guide

### Interacting with the Barista

Simply type natural language queries in the chat:

- "Show me cold drinks"
- "I'm lactose intolerant, what can I have?"
- "What pastries do you have?"
- "I want something strong and hot"
- "Do you have anything vegan?"

### Using the Shopping Cart

1. **Add items** - Click "Add to Cart" from the menu sidebar or recommended items in chat
2. **Adjust quantities** - Use +/- buttons in the cart
3. **Checkout** - Click "Checkout" when ready to complete your order
4. **Clear cart** - Remove all items with "Clear Cart"

### Menu Categories

- **Coffee** - Espresso drinks, cold brew, lattes
- **Bakery** - Pastries and baked goods
- **Specialty** - Seasonal and special items

---

## Project Structure

```
coffee-shop-ai-barista/
├── app.py              # Main Streamlit application
├── agent.py            # AI agent (OpenRouter integration)
├── menu_search.py      # Menu filtering and search
├── cart_manager.py     # Shopping cart operations
├── config.py           # Configuration and env loading
├── requirements.txt    # Python dependencies
├── .env                # API keys (not in git)
├── .env.example        # Template for API keys
├── .gitignore          # Git ignore rules
├── screenshots/        # App screenshots
└── data/
    ├── menu.json       # Coffee shop menu
    └── orders.json     # Order history (generated)
```

---

## Screenshots

### Chat Interface

![Chat Interface](screenshots/Screenshot%202026-10-29%20171227.png)

### Menu & Cart Sidebar

![Menu and Cart Sidebar](screenshots/Screenshot%202026-10-29%20171250.png)

### Order Checkout

![Order Checkout](screenshots/Screenshot%202026-10-29%20171303.png)

---

## Customization

### Edit the Menu

Modify `data/menu.json` to add/remove items:

```json
{
  "id": 9,
  "name": "Matcha Latte",
  "description": "Ceremonial grade matcha with steamed milk",
  "price": 5.50,
  "category": "specialty",
  "tags": ["sweet", "hot", "dairy-free-option"],
  "allergens": ["dairy"]
}
```

### Change AI Model

Edit `agent.py` and modify the model parameter to any model from [openrouter.ai/models](https://openrouter.ai/models):

```python
model="openai/gpt-4o-mini"  # Any OpenRouter model ID
```

### Add Menu Categories

Categories are automatically detected from menu items. Just add a new `category` value to items in `menu.json`.

---

## Troubleshooting

**'streamlit' is not recognized as a command**
- Run via Python module instead:
  ```bash
  python -m streamlit run app.py
  ```
- Add Python Scripts directory to PATH:
  - Windows: `C:\Users\<YourUser>\AppData\Local\Programs\Python\Python3X\Scripts\`

**API Key Errors**
- Ensure `.env` file exists and contains a valid OpenRouter API key
- OpenRouter keys start with `sk-or-`
- Get your key at https://openrouter.ai/keys

**Model Not Available**
- The model ID may have changed or been removed from OpenRouter
- Browse current free models at https://openrouter.ai/models and update `agent.py:92`

**Missing Dependencies**
- Run `pip install -r requirements.txt` again
- Ensure Python 3.8+ is installed

**Port Already in Use**
- Run on different port: `streamlit run app.py --server.port 8502`

---

## Future Enhancements

- Order status tracking (Preparing → Ready → Picked Up)
- Customer accounts and loyalty points
- Sales analytics dashboard
- Multiple language support
- Order receipt generation (PDF)
- Voice input support

---

## License

This project is for educational and demonstration purposes.
