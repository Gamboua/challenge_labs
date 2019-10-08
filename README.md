## Installation

**PYTHON >= 3.7.0**

Install dependencies:
```
make dependencies
```

Run migrations:
```
make migrate
```

## Testing
Run tests:
```
make test

or

make test-matching -k some-piece-of-text
```

Run code lint:
```
make lint
```

Run fix python imports:
```
make fix-python-import
```

## Server

Run project:
```
make run
```

## API - Authentication

Create an client_id and secret:
```
make create-app name=choose-a-good-name
```

List app (you can retrieve your valid token here)
```
make list-apps
```

## DOCS

Get token by URL:
```
POST application/token/

Content-Type: application/json

{
	"client_id": "id",
	"client_secret": "secret"
}

```

[CUSTOMER API](docs/api/customer.md)
