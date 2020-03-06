# pm-sls-alerter

### Outline

This project checks the Prime Ministers of Australia from Wikipedia and sends alerts if their political party affiliation has been changed.

### Deployment

 * Replace the SNS topic ARN with one in your account
 * Create a DynamoDB table called 'prime_ministers', with primary key 'name' and attribute 'party'
 * Populate the table with two entries: 'Sir Edmund Barton' and 'Alfred Deakin'
 * Ensure you have Docker installed and running on your local machine - it is required to build a container to package the required Python modules
 * Create a Python virtualenv
 * Run 'pip install'
 * Run 'npm install'
 * Run 'serverless deploy'
 * It is also recommended to replace the FullAccess policies in serverless.yml with custom policies that have narrower permission scopes