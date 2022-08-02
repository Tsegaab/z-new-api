# Z-News-Aggregator


Simple application to aggregate newd from mulitple sources.

**Designed to easly add mode news API sources.**

It is made simple to add additional APIs, to do that the developed only need to expted `BaseAPI` class implement as constrained and add the new API class to `SOURCE_APIS` in `main.py`.


## Local setup steps
**Python3 required.**
1. Clone this project to local directory
2. Create virtual environment and activate.
    ```shell
    python3 -m venv venv
    source venv/bin/activate
    ````
3. Install dependency packages.
    ```shell
    pip install -r requirements.txt
    ```
4. Update `settings.py` file, add News API and Reddit API credentials.

5. Run API service.
    ```shell
    uvicorn main:api
    ``` 