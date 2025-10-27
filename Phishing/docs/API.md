"""# API Documentation

## Campaign Statistics

**Endpoint:** `/api/campaign/<campaign_id>/stats`

**Method:** GET

**Response:**
```json
{
    "name": "Q1 Security Training",
    "total_targets": 100,
    "sent": 100,
    "opened": 75,
    "clicked": 25,
    "submitted": 8,
    "open_rate": 75.0,
    "click_rate": 25.0,
    "submit_rate": 8.0
}
```

## Future Endpoints

- POST `/api/campaign/create` - Create campaign
- GET `/api/campaigns` - List campaigns
- POST `/api/template/create` - Create template
"""