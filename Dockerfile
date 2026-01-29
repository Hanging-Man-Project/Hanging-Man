# 1. Utilisation d'une image de base légère
FROM python:3.13.1-slim

# 2. Définition du répertoire de travail
WORKDIR /app

# 3. Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie du code source
COPY . .

# 5. Sécurité : Ne pas exécuter en tant que root
RUN useradd -m devopsuser
USER devopsuser

# 6. Documentation du port
EXPOSE 8080

# 7. Lancement de l'application
CMD ["python", "app.py"]

#docker build -t image_exo_2 .
#docker run -p 8080:8080 image_exo_2