FROM python
WORKDIR /todo_flask_app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "run.py"]
