# MandiGPT Deployment Guide

## 🚀 Quick Deployment

### Local Development

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd mandigpt
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Copy example config
   cp config_example.py config.py
   
   # Edit config.py with your API keys
   OPENWEATHER_API_KEY = "your_api_key_here"
   ```

3. **Run Tests**
   ```bash
   python test_mandigpt.py
   ```

4. **Start Application**
   ```bash
   python run.py
   # or
   python main.py
   ```

5. **Access Application**
   - Web Interface: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Production Deployment

#### Using Docker

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   EXPOSE 8000
   
   CMD ["python", "main.py"]
   ```

2. **Build and Run**
   ```bash
   docker build -t mandigpt .
   docker run -p 8000:8000 -e OPENWEATHER_API_KEY=your_key mandigpt
   ```

#### Using Cloud Platforms

##### Heroku Deployment

1. **Create Procfile**
   ```
   web: python main.py
   ```

2. **Set Environment Variables**
   ```bash
   heroku config:set OPENWEATHER_API_KEY=your_key
   heroku config:set DEBUG=False
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

##### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.micro or larger
   - Security group: HTTP (80), HTTPS (443), SSH (22)

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

4. **Run with Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 main:app
   ```

##### Google Cloud Platform

1. **Create App Engine Configuration**
   ```yaml
   # app.yaml
   runtime: python39
   
   env_variables:
     OPENWEATHER_API_KEY: "your_key"
     DEBUG: "False"
   
   handlers:
   - url: /.*
     script: auto
   ```

2. **Deploy**
   ```bash
   gcloud app deploy
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Yes | - |
| `COMMODITY_API_KEY` | Commodity price API key | No | Mock data |
| `DEBUG` | Debug mode | No | True |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |

### API Keys Setup

#### OpenWeatherMap API
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Set in environment variables

#### Commodity Price API (Optional)
- Currently uses mock data
- Can integrate with real commodity APIs
- Set `COMMODITY_API_KEY` if available

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Logs
```bash
# View application logs
tail -f logs/mandigpt.log

# View error logs
tail -f logs/error.log
```

### Performance Monitoring
- Monitor API response times
- Track weather API usage
- Monitor commodity price updates

## 🔒 Security

### Production Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS with SSL certificates
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Validate all inputs
- [ ] Use environment variables for secrets
- [ ] Regular security updates

### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/recommendations")
@limiter.limit("10/minute")
async def get_recommendations(request: Request, query: FarmerQuery):
    # Your code here
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**
   ```
   Error: Invalid API key
   Solution: Check OPENWEATHER_API_KEY environment variable
   ```

2. **Port Already in Use**
   ```
   Error: Address already in use
   Solution: Change PORT in config or kill existing process
   ```

3. **Missing Dependencies**
   ```
   Error: ModuleNotFoundError
   Solution: pip install -r requirements.txt
   ```

4. **Weather API Limits**
   ```
   Error: API rate limit exceeded
   Solution: Implement caching or upgrade API plan
   ```

### Debug Mode
```bash
# Enable debug logging
export DEBUG=True
python main.py
```

## 📈 Scaling

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Multiple application instances
- Database clustering if needed

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching

### Caching Strategy
```python
from functools import lru_cache
import redis

# In-memory caching
@lru_cache(maxsize=100)
def get_crop_suitability(crop, location, weather):
    # Your code here

# Redis caching
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_weather_data(location, data):
    key = f"weather:{location.latitude}:{location.longitude}"
    redis_client.setex(key, 3600, json.dumps(data))  # 1 hour cache
```

## 🔄 Updates

### Rolling Updates
1. Deploy new version to staging
2. Run tests
3. Deploy to production
4. Monitor for issues
5. Rollback if needed

### Database Migrations
- Update agricultural database
- Migrate crop data
- Update regional information

## 📞 Support

For deployment issues:
- Check logs: `tail -f logs/mandigpt.log`
- Test API: `curl http://localhost:8000/health`
- Run diagnostics: `python test_mandigpt.py`

---

**Happy Farming! 🌾**
