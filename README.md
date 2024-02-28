# Currency Conversion API 


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

    ```plaintext
    API_TOKEN=your-exchange-api-token
    ```
   to get API_TOKEN visit : [ExchangeRateAPI](https://www.exchangerate-api.com/)


4. Build and run the Docker containers:

    ```bash
    make run
    ```

This will build the project and start the Docker containers. Other container commands in Makfile

## API Endpoints
- API is built using [FastAPI](https://fastapi.tiangolo.com/).


- Get Last Update
   ```bash
   curl http://localhost:8000/api/concurrency_conversion/last_update/{currency_name}
   ```

- Update Currency
   ```bash
   curl http://localhost:8000/api/concurrency_conversion/update/{currency_name}
   ```

- Convert Currency
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"source_currency": "USD", "target_currency": "EUR", "amount": 100}' http://localhost:8000/api/concurrency_conversion/convert
   ```

## Run Tests

   ```
   docker exec -it api /bin/bash
   pytest tests/
   ```
