
# FastAPI Project

This is a FastAPI project setup guide. Follow the steps below to get your development environment up and running.

## Prerequisites

- [Poetry](https://python-poetry.org/docs/#installation)
- [Stripe CLI](https://docs.stripe.com/stripe-cli)
- [ngrok](https://ngrok.com/download)

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/EmileIB/monty-assignment.git
cd monty-assignment
```

2. **Install dependencies**

```bash
poetry install
```

3. **Create a `.env` file**

Copy the example environment file and fill in the required details.

```bash
cp .env.example .env
```

Edit the `.env` file and add your `MONGO_URL`, `DB_NAME`, `SECRET_KEY`, `ALGORITHM` and `ACCESS_TOKEN_EXPIRE_MINUTES`

### Note
To generate a unique `SECRET_KEY`, you may use the following command:
```bash
openssl rand -hex 32
```

## Stripe Setup

1. **Create a Stripe account**

   - Sign up at [Stripe](https://stripe.com/).

2. **Get your secret key**

   - Add the secret key to your `.env` file under `STRIPE_SECRET_KEY`.

3. **Install and configure Stripe CLI**

```bash
stripe login
```

Follow the steps to authenticate.

4. **Start Stripe webhook listener**

```bash
stripe listen --forward-to http://127.0.0.1:8000/v1/stripe/webhook
```

When you get the webhook secret, add it to your `.env` file under `WEBHOOK_SECRET`.

## ngrok Setup

1. **Install and configure ngrok**

   - Follow the installation instructions at [ngrok](https://ngrok.com/download).

2. **Start ngrok**

```bash
ngrok http 8000
```

3. **Update `.env` file**

   - Set the `UPLOADS_URL` inside `.env` to `ngrok_url/uploads` (replace `ngrok_url` with the URL provided by ngrok).

## Admin User Setup

Inside the `.env` file, you will see `ADMIN_USERNAME` and `ADMIN_PASSWORD`. These are the default admin credentials created on application startup. Fill in the desired values.

## Running the Server

To start the server, use the following command:

```bash
uvicorn app.main:app --reload
```

## API Documentation

To view the API documentation, navigate to:

[http://localhost:8000/docs](http://localhost:8000/docs)
