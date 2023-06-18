# Custom Memory Database(Flask)

# Installation:

### Using Docker

```bash
docker build -t custom-memory .
docker run -p 5000:5000 custom-memory
```

# using VirtualEnv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app main run --debug


# Available Endpoints
 - POST /submit
    ```bash
    {
        title: string
        author: string
        text: string
        url: string
    }```

 - GET /item/<str:item_id>
 - GET /search?title=<string>&author=<string>
 - GET /rss?title=<string>&author=<string>
    

## Video Demos

[From Generator](https://www.loom.com/share/0c4d96e34eef4957b3a7004ddc2b7687?sid=daf924d4-b617-4781-8bbd-56fb5311ec64)
[From Postman](https://www.loom.com/share/77bb13f9953d4d359aee60ed6ebd2a64?sid=21e82245-7f19-4025-b0cf-972973b55f9d)
