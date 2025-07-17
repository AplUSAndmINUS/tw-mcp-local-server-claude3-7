# API Documentation

This document provides comprehensive information about the TW MCP Local Server API endpoints and usage.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication for local usage. For production deployments, consider implementing API key authentication.

## Common Response Format

All API responses follow this general structure:

```json
{
  "content": "The response content",
  "usage": {
    "input_tokens": 123,
    "output_tokens": 456,
    "total_tokens": 579
  },
  "model": "claude-3-sonnet-20240229",
  "role": "assistant",
  "stop_reason": "end_turn"
}
```

## Endpoints

### Health Check

Check if the server is running and healthy.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "timestamp": 1640995200.0,
  "version": "0.1.0",
  "claude_status": true,
  "plugins_loaded": 1
}
```

### Text Completion

Generate text completions using Claude.

**Endpoint**: `POST /complete`

**Request Body**:
```json
{
  "prompt": "Help me write a Python function",
  "system_prompt": "You are a helpful programming assistant",
  "context": {
    "language": "python",
    "difficulty": "beginner"
  },
  "max_tokens": 1000,
  "temperature": 0.7,
  "stream": false
}
```

**Response**:
```json
{
  "content": "Here's a Python function that...",
  "usage": {
    "input_tokens": 25,
    "output_tokens": 150,
    "total_tokens": 175
  },
  "model": "claude-3-sonnet-20240229",
  "role": "assistant",
  "stop_reason": "end_turn"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/complete \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a hello world function in Python",
    "max_tokens": 500
  }'
```

### Vibe Coding

Get empathetic, thoughtful programming assistance.

**Endpoint**: `POST /vibe-code`

**Request Body**:
```json
{
  "request": "I'm struggling with async/await in Python",
  "context": {
    "mood": "supportive",
    "experience_level": "beginner",
    "focus": "learning"
  },
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "content": "I understand that async/await can be confusing at first...",
  "usage": {
    "input_tokens": 30,
    "output_tokens": 300,
    "total_tokens": 330
  },
  "model": "claude-3-sonnet-20240229",
  "role": "assistant",
  "stop_reason": "end_turn"
}
```

**Context Options**:
- `mood`: `supportive`, `encouraging`, `analytical`, `creative`
- `experience_level`: `beginner`, `intermediate`, `advanced`
- `focus`: `general`, `performance`, `readability`, `architecture`

### Chat Conversation

Have multi-turn conversations with Claude.

**Endpoint**: `POST /chat`

**Request Body**:
```json
{
  "messages": [
    {"role": "user", "content": "What's the difference between lists and tuples?"},
    {"role": "assistant", "content": "Lists are mutable while tuples are immutable..."},
    {"role": "user", "content": "Can you show me an example?"}
  ],
  "system_prompt": "You are a patient programming tutor",
  "max_tokens": 1500,
  "temperature": 0.7
}
```

**Response**:
```json
{
  "content": "Of course! Here's a simple example...",
  "usage": {
    "input_tokens": 45,
    "output_tokens": 200,
    "total_tokens": 245
  },
  "model": "claude-3-sonnet-20240229",
  "role": "assistant",
  "stop_reason": "end_turn"
}
```

### Code Analysis

Analyze and improve code with Claude.

**Endpoint**: `POST /analyze-code`

**Request Body**:
```json
{
  "code": "def process_data(data):\n    result = []\n    for item in data:\n        if item > 0:\n            result.append(item * 2)\n    return result",
  "language": "python",
  "task": "improve",
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Task Options**:
- `analyze`: General code analysis
- `review`: Code review for bugs and quality
- `improve`: Suggest improvements
- `debug`: Help debug issues

**Response**:
```json
{
  "content": "Here's an improved version of your code...",
  "usage": {
    "input_tokens": 50,
    "output_tokens": 250,
    "total_tokens": 300
  },
  "model": "claude-3-sonnet-20240229",
  "role": "assistant",
  "stop_reason": "end_turn"
}
```

### Plugin Information

Get information about loaded plugins.

**Endpoint**: `GET /plugins`

**Response**:
```json
{
  "plugins": [
    {
      "name": "vibe_coder",
      "version": "1.0.0",
      "description": "Empathetic programming companion",
      "author": "AplUSAndmINUS",
      "enabled": true
    }
  ]
}
```

### Server Settings

Get current server configuration (excluding sensitive data).

**Endpoint**: `GET /settings`

**Response**:
```json
{
  "host": "localhost",
  "port": 8000,
  "debug": false,
  "claude_model": "claude-3-sonnet-20240229",
  "max_tokens": 4096,
  "temperature": 0.7,
  "enabled_plugins": ["vibe_coder"],
  "log_level": "INFO"
}
```

## Plugin-Specific Endpoints

### Vibe Coder Plugin

The vibe coder plugin provides additional endpoints:

**Endpoint**: `POST /vibe/code`

**Request Body**:
```json
{
  "request": "Help me write a sorting algorithm",
  "context": {
    "project_type": "learning",
    "deadline": "relaxed"
  },
  "mood": "encouraging",
  "focus": "learning",
  "experience_level": "intermediate"
}
```

**Response**:
```json
{
  "response": "I'd be happy to help you with sorting algorithms...",
  "suggestions": [
    "Start with bubble sort for learning",
    "Consider quicksort for efficiency",
    "Python's built-in sort() is optimized"
  ],
  "resources": [
    "Python Official Documentation",
    "Algorithm Visualization Tools",
    "Practice Problems"
  ],
  "confidence": 0.85,
  "reasoning": "Based on your intermediate level and learning focus..."
}
```

**Code Review**: `POST /vibe/review`
**Code Explanation**: `POST /vibe/explain`

## Error Handling

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request
- `401`: Unauthorized
- `429`: Rate Limited
- `500`: Internal Server Error

**Error Response Format**:
```json
{
  "detail": "Error message describing what went wrong",
  "type": "error_type",
  "status_code": 400
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Default**: 100 requests per minute
- **Headers**: Rate limit information is included in response headers
- **Exceeded**: Returns `429 Too Many Requests`

**Rate Limit Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995260
```

## Streaming Responses

For long responses, you can enable streaming:

**Request**:
```json
{
  "prompt": "Write a detailed explanation of machine learning",
  "stream": true
}
```

**Response**: Server-Sent Events (SSE) format
```
data: {"chunk": "Machine learning is..."}
data: {"chunk": " a subset of artificial intelligence..."}
data: {"done": true}
```

## WebSocket Support

For real-time interactions, WebSocket support is available:

**Endpoint**: `ws://localhost:8000/ws/chat`

**Message Format**:
```json
{
  "type": "message",
  "content": "Hello, can you help me with coding?",
  "context": {
    "mood": "supportive"
  }
}
```

## SDK Examples

### Python SDK

```python
import asyncio
import httpx

class MCPClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def vibe_code(self, request, **kwargs):
        response = await self.client.post(
            f"{self.base_url}/vibe-code",
            json={"request": request, **kwargs}
        )
        return response.json()
    
    async def complete(self, prompt, **kwargs):
        response = await self.client.post(
            f"{self.base_url}/complete",
            json={"prompt": prompt, **kwargs}
        )
        return response.json()

# Usage
async def main():
    client = MCPClient()
    result = await client.vibe_code(
        "Help me understand Python decorators",
        mood="supportive",
        experience_level="beginner"
    )
    print(result["content"])

asyncio.run(main())
```

### JavaScript SDK

```javascript
class MCPClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async vibeCode(request, options = {}) {
        const response = await fetch(`${this.baseUrl}/vibe-code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ request, ...options })
        });
        return response.json();
    }
    
    async complete(prompt, options = {}) {
        const response = await fetch(`${this.baseUrl}/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt, ...options })
        });
        return response.json();
    }
}

// Usage
const client = new MCPClient();
client.vibeCode('Help me with async JavaScript', {
    mood: 'encouraging',
    experience_level: 'intermediate'
}).then(result => {
    console.log(result.content);
});
```

## OpenAPI/Swagger Documentation

The server provides interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Best Practices

1. **Use appropriate context**: Provide relevant context for better responses
2. **Set reasonable limits**: Use appropriate `max_tokens` values
3. **Handle errors gracefully**: Always check response status codes
4. **Respect rate limits**: Implement client-side rate limiting
5. **Use streaming for long responses**: Enable streaming for better UX
6. **Provide feedback**: Include user experience level and preferences

## Examples

See the [examples](../examples/) directory for complete working examples of API usage.