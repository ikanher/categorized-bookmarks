FROM python

WORKDIR /opt/categorized-bookmarks
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/ikanher/categorized-bookmarks .
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate"
RUN pip install -r requirements.txt
CMD ["gunicorn", "--preload", "--bind", "0.0.0.0:80", "--workers", "1", "application:app"]
