from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
import openai
from database import get_db, Product, create_tables, seed_database

load_dotenv()

app = FastAPI(title="E-commerce Chatbot API")

# Create tables and seed data on startup
create_tables()
seed_database()

# Configure OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

def get_all_products(db: Session) -> List[Product]:
    return db.query(Product).all()

def format_products_for_prompt(products: List[Product]) -> str:
    product_list = []
    for product in products:
        product_list.append(f"- {product.name}: {product.description} (Category: {product.category}, Price: ${product.price})")
    return "\n".join(product_list)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Get all products from database
        products = get_all_products(db)
        products_text = format_products_for_prompt(products)
        
        # Create system prompt
        system_prompt = f"""You are a helpful e-commerce assistant. Your job is to recommend products from our catalog based on user queries.

Available products:
{products_text}

Instructions:
1. When a user asks about products, recommend the most relevant ones from the catalog above
2. Include the product name, description, and price in your response
3. If no exact match is found, suggest popular or similar alternatives from the catalog
4. Keep responses concise and helpful
5. Format your response in a friendly, conversational way
6. Always recommend actual products from the catalog provided above"""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content.strip()
        
        return ChatResponse(response=bot_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    with open("static/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9876)