#main.py

from fastapi import FastAPI, Query, File, UploadFile, HTTPException
from src import MovieInput, MovieResponse, CSVInfo, DataStorage
import logging
from pathlib import Path
import io
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


#a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int): #type annotation: it declares the expected type, int
    return {"requested_id": movie_id}


#a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    #The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}


@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump()

demo_movie_examples = []

@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record

@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read() # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename,"size_bytes": len(contents)}

@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}


@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    record = list(movies.values())[:limit]
    logger.info(f"Returned {len(record)} movies")
    return record


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    movie_id = len(movies) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    movies[movie_id] = record
    logger.info(f"New movie ID: {movie_id}")
    return record

storage = DataStorage()

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    filename = Path(file.filename)
    if filename.suffix.lower() != ".csv":
        logger.warning(f"File extension {filename.suffix} not accepted")
        raise HTTPException(status_code=400, detail="Must be CSV file")

    contents = await file.read()
    
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError,pd.errors.ParserError,UnicodeDecodeError) as error:
        logger.warning(f"Cannot read CSV: {error}")
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")

    dataset_id = storage.save_data(df, filename.name)
    logger.info(f"Saved dataset id={dataset_id}, filename={filename.name}")

    return CSVInfo(
        dataset_id=dataset_id,
        filename=filename.name,
        rows=df.shape[0],
        columns=df.shape[1],
        column_names=df.columns.tolist()
    )

@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    df = storage.get_data(dataset_id)
    if df is None:
        logger.warning(f"Dataset ID {dataset_id} not found")
        raise HTTPException(status_code=404, detail="Dataset not found")

    logger.info(f"Retrieved dataset {dataset_id}")
    return {"id": dataset_id, "rows": df.shape[0], "columns": df.shape[1]}