![](https://www.politico.com/interactives/cdn/images/badge.svg)

# django-slack-events-router

[![PyPI version](https://badge.fury.io/py/django-slack-events-router.svg)](https://badge.fury.io/py/django-slack-events-router)

### Why this?

Pinching pennies and hanging on to the free version of Slack? You're likely very aware of [the limit](https://get.slack.help/hc/en-us/articles/115002422943-Message-file-storage-and-app-limits-on-the-Free-plan) Slack places on the number of custom apps you can install in your free Slack team. Since each app is also limited to one endpoint for receiving events from the Slack Events API, you may already be juggling your custom integrations or stopped building new ones altogether.

django-slack-events-router lets you extend your use of free Slack by creating an events router to send Slack Events API messages to any number of endpoints via custom webhook routes. You can then configure filters for your custom routes based on event type or channel, giving you a powerful way to filter the Event API's firehose to just the messages your downstream apps need.

### Installation

1. Install the app.

  ```
  $ pip install django-slack-events-router
  ```

2. Run migrations
  ```
  $ python manage.py migrate
  ```

3. [Configure an app in Slack](#configuring-your-app-in-slack), get its [signing secret](https://api.slack.com/docs/verifying-requests-from-slack#app_management_updates) and export it as the environment variable `SLACK_SIGNING_SECRET`.

4. Add the app to your Django project and configure settings, including a verification token other apps can use to access the eventsrouter's own API.

  ```python
  # settings.py
  INSTALLED_APPS += [
      'rest_framework',
      'eventsrouter',
  ]

  EVENTSROUTER_VERIFICATION_TOKEN = 'A_VERIFICATION_TOKEN'
  ```

5. Configure the app's URL root.

  ```python
  # urls.py
  urlpatterns += [
      path("events-router", include("eventsrouter.urls")),
  ]
  ```

### Usage

Once you've installed and configured the eventsrouter app, you can register downstream apps that will receive your re-routed Slack Events API messages. Just create a new Route model manually via the django admin or programmatically using the eventsrouter's API.

When you do, you can also create filters for your route to send only events of a certain type or from a particular channel. Exclude both to send all event messages. (Remember, you also need to register events with your Slack app before they'll be sent to the eventsrouter! See [Configuring your app in Slack](#configuring-your-app-in-slack).)

The goal is that downstream applications should be able to accept messages from eventsrouter using the same code they would use if they were pointed directly at the Events API.

That means the eventsrouter simply forwards the payload Slack sends, including  signing secret headers. (We recommend your app verify messages, see [Verifying messages from Slack](#verifying-messages-from-slack).)

### Verifying messages from Slack

eventsrouter will verify messages come from Slack using your app's [signing secret](https://api.slack.com/docs/verifying-requests-from-slack), which should be exported as the environment variable `SLACK_SIGNING_SECRET`.

When it routes messages to the endpoints in your Route models, it will resend the `X-Slack-Signature` and `X-Slack-Request-Timestamp` headers with the payload so your downstream app can also verify messages.

We recommend using the [utility functions](https://the-politico.github.io/politico-toolbox/toolbox/slack/verify.html) in our [`politico-toolbox`](https://github.com/The-Politico/politico-toolbox) app to verify messages. See also the custom authentication methods for [Django Rest Framework](https://the-politico.github.io/politico-toolbox/toolbox/django/rest/authentication/slack.html) and [Flask](https://the-politico.github.io/politico-toolbox/toolbox/flask/authentication/slack.html).

### Configuring your app in Slack

1. Create [a new app](https://api.slack.com/slack-apps) for your team in Slack.

2. Grab your app’s [signing secret](https://api.slack.com/docs/verifying-requests-from-slack).

![](https://a.slack-edge.com/779d2/img/api/signing_secrets_admin_page.png)

3. Enable [events subscriptions](https://api.slack.com/events-api) in your app and configure the Request URL to hit eventsrouter's `/events/` endpoint. (Your app will need to be deployed in order to verify the URL with Slack.)

4. Subscribe to all the workspace events you want to route downstream.

### Developing

##### Running a development server

Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/eventsrouter"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
