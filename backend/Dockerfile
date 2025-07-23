FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos necessários
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta que será usada pela FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]