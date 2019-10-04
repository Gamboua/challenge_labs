## Installation
Install dependencies:
```
make dependencies
```

Run migrations:
```
make migrate
```

Create an app:
```
make create-app name=<choose a good name>
```

List app (you can get a valid token here)
```
make list-apps
```

## API

Get token:
```
POST application/token/

Content-Type: application/json

{
	"client_id": "id",
	"client_secret": "secret"
}

```
