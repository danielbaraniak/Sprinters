# Sprinters

Competence project

## Instalation

1. Create and run a virtual environment

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

1. Install all requirements

    ```bash
    pip3 install -r requirements.txt
    ```

1. Create a file `settings.cfg`:

    1. Find a file [`template_settings.cfg`](/template_settings.cfg)
    1. Copy it and rename to `settings.cfg`
    1. Fill in necessary settings. [Learn More](/webservice/README.md#settings)

## Usage

- Training a model

    ```bash
    python3 -m launch --train
    ```

    About [model configuration](/ml/README.md#generating-models).

- Run flask application

    ```bash
    python3 -m launch --web
    ```
    
- [How to use frontend?](frontend/README.md)

- Start scraping worker
    ```bash
    python3 -m launch --scrape
    ```

    [Certain info about scraping worker](scraper/README.md)
