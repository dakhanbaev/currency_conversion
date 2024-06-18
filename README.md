# Content Analysis Service


- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Run Tests](#run-tests)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/dakhanbaev/currency_conversion.git
    ```

2. Navigate to the project directory:

    ```bash
    cd currency_conversion
    ```

3. Create a `.env` file in the root of the project and set the required environment variables. You can use the provided `env-file` as a template.



4. Build and run the Docker containers:

    ```bash
    make run
    ```

This will build the project and start the Docker containers. Other container commands in Makfile

## API Endpoints
- API is built using [FastAPI](https://fastapi.tiangolo.com/).


- Run analyze task
   ```bash
    curl -X POST \
     -F "file=image.jpeg" \
     -F "description=Some description" \
     http://localhost:8000/analysis
    ```

- Get analyze result
   ```bash
   curl http://localhost:8000/api/analysis/{request_id}
   ```
  
- Get analyze result with frame number for video
   ```bash
   curl http://localhost:8000/api/analysis/{request_id}/{frame}
   ```

- Delete analyze result
   ```bash
   curl -X DELETE http://localhost:8000/api/analysis/{request_id}
  ```

## Run Tests

   ```
   docker exec -it api /bin/bash
   pytest tests/
   ```
