# Running in Docker

## Get the image

```bash
docker pull ikanher/categorized-bookmarks
```

## Running

### Development mode

To run in development mode, with SQLite database, use

```bash
docker run -e 'FLASK_ENV=development' --rm -p 5000:80 -d ikanher/categorized-bookmarks
```

The app will listen for connections at [localhost port 5000](http://localhost:5000/).

### Production mode

To run in development mode, with PostgreSQL database, use

```bash
docker run -e 'DATABASE_URL=<insert your postgres uri here>' --rm -p 5000:80 -d ikanher/categorized-bookmarks
```

The app will listen for connections at [localhost port 5000](http://localhost:5000/).
