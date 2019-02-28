![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-slack-events-router

### Usage
Slack Events Router gives you access to `Route` models which are endpoints that will receive Slack payloads as they come in. In order to save on server load, this app also comes with the ability to only route payloads concerning a particular channel or event.

Channels must be created in the Django admin or via REST API before they can be added as a route filter.

Events can be selected from a pre-filled list (but keep in mind that these events must be registered to in the Slack app to even get to the router app). So selecting `reaction_added` as an event_filter in your `Route` does not mean those payloads will make it to your endpoint if your slack app isn't also subscribed to the `reaction_added` workspace event. See [Configure Your Slack App](#configure-your-slack-app) for more.

### Installation

1. Install the app.

  ```
  $ pip install django-slack-events-router
  ```

2. Run migrations
  ```
  $ python manage.py migrate
  ```

3. [Configure Your Slack App](#configure-your-slack-app) and get its verification token.

4. Add the app to your Django project and configure settings.

  ```python
  # settings.py
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'eventsrouter',
  ]

  #########################
  # eventsrouter settings

  EVENTSROUTER_SLACK_VERIFICATION_TOKEN = ''
  ```

5. Configure the app's URL root.

  ```python
  # urls.py
  urlpatterns = [
      ...

      path("events-router", include("eventsrouter.urls")),
  ]
  ```

### Configuring Your Slack App

1. Create [a new app](https://api.slack.com/slack-apps) for your team in Slack.

2. Grab your app’s [verification token](https://api.slack.com/docs/token-types#verification_tokens) (for EVENTSROUTER_SLACK_VERIFICATION_TOKEN).

![](https://django-slackchat-serializer.readthedocs.io/en/latest/_images/verification.png)

3. Enable [events subscriptions](https://api.slack.com/events-api) in your app and configure the Request URL to hit events-router's `/events/` endpoint. (Your app will need to be installed and running in order to verify the URL with Slack.)

4. Subscribe to all the workspace events you want to route.

### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd eventsrouter/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
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
