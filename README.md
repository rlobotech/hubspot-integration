# HubSpot Integration
This application integrates with HubSpot to manage contacts. It supports batch processing of contact data, handles rate limits, and utilizes HubSpot's upsert API to efficiently create or update contacts.

## Requirements
Ensure you have **Python 3.7+** and **pip** installed. You can install the required dependencies using the following commands:

```sh
sudo apt install python3.7 -y
sudo apt install python3-pip -y
pip install -r requirements.txt
```

## Environment Variables Setup
Before running the application, you need to set up your environment variables. You can either export them directly in your terminal or create a `.env` file in the root directory of the project.

### Option 1: Set environment variables directly

```sh
export HUBSPOT_API_KEY="key_here"
export AWS_ACCESS_KEY="key_here"
export AWS_PROD_URL="root_url_here"
```

### Option 2: Create a `.env` file
Create a `.env` file in the root directory of the project and add the following lines:

```ini
HUBSPOT_API_KEY=key_here
AWS_ACCESS_KEY=key_here
AWS_PROD_URL=root_url_here
```

Replace `key_here` and `url_here` with your actual HubSpot API key, AWS access key, and AWS production URL **(without `/contacts`)**.

## Running the Application
Once dependencies are installed and environment variables are set, you can run the application with:

```sh
python main.py
```

## Application Notes

- Multithreading: The app is configured to use up to 10 workers for concurrent processing of contact data.
- Upsert API Request: The app uses HubSpot's upsert API request to create or update contacts based on email addresses.
- Email as Unique Identifier: Contacts are uniquely identified by their email for updates. This decision is open to modification based on the Business Rules.
- AWS Data Processing: Contacts that do not have an email address are excluded from processing. This is also an operational choice that can be altered based on the Business Rules.

### Business Rules

All the app's operational decisions could be changed based on the Business Rules.

## Running Unit Tests
To run the unit tests, use the following command:

```sh
PYTHONPATH=./ pytest
```

This command sets the PYTHONPATH to the current directory (./) and runs the tests using pytest.

## Batch Limits
HubSpot batch operations are limited to **100 records per batch request**. This value can be adjusted in `settings.py`, but it **must not exceed 100** to comply with HubSpot’s restrictions.

For more details, refer to the official documentation:
[HubSpot API Batch Limits](https://developers.hubspot.com/docs/guides/api/crm/objects/contacts#limits)

## Rate Limits
- **100 private app requests every 10 seconds** (lowest tier).
- If the rate limit is reached, the system implements an **exponential backoff retry mechanism**.

For more details, refer to the official HubSpot API rate limits:
[HubSpot API Rate Limits](https://developers.hubspot.com/docs/guides/apps/api-usage/usage-details#request-limits)
