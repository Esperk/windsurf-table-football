# Table Football Tracker

A modern web application for tracking table football (foosball) matches, built with Django, Python, and Docker. The app features Google OAuth authentication and a flashy, animated user interface.

![Table Football Tracker](https://img.shields.io/badge/Table%20Football-Tracker-blue)
![Django](https://img.shields.io/badge/Django-4.2.10-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## Features

- **Match Tracking**: Record matches with 2, 3, or 4 players (1v1, 2v1, or 2v2 formats)
- **Player Statistics**: Automatically calculated stats including wins, losses, goals, and win percentage
- **Leaderboard**: See who's the champion with a dynamic leaderboard
- **Google OAuth**: Secure authentication using Google accounts
- **Responsive Design**: Works on desktop and mobile devices
- **Animations**: Modern UI with smooth animations and transitions
- **Docker Support**: Easy deployment with Docker and Docker Compose

## Screenshots

(Add screenshots of your application here once deployed)

## Installation

### Prerequisites

- Docker and Docker Compose
- Google OAuth credentials (Client ID and Client Secret)

### Setup Instructions

1. **Clone the repository**

```bash
git clone <repository-url>
cd table_football_app
```

2. **Configure environment variables**

Create a `.env` file in the root directory with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key-replace-in-production
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret
```

3. **Build and run with Docker Compose**

```bash
docker-compose up --build
```

Alternatively, you can use the provided Make commands:

```bash
# Build and start the application
make docker-build
make docker-up

# Or simply run the development server
make runserver
```

4. **Create a superuser (admin account)**

In a new terminal window, run:

```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Access the application**

Open your browser and navigate to:
- Application: http://localhost:8000
- Admin interface: http://localhost:8000/admin

## Setting up Google OAuth

1. Go to the [Google Developer Console](https://console.developers.google.com/)
2. Create a new project
3. Navigate to "Credentials" and create OAuth client ID credentials
4. Configure the OAuth consent screen
5. Add authorized redirect URIs:
   - http://localhost:8000/accounts/google/login/callback/
   - https://yourdomain.com/accounts/google/login/callback/ (for production)
6. Copy the Client ID and Client Secret to your `.env` file

## Usage Guide

### Recording a Match

1. Log in with your Google account
2. Click on "New Match" in the navigation bar
3. Select the match type (1v1, 2v1, or 2v2)
4. Choose the players for each team
5. Enter the final score
6. Add optional notes about the match
7. Submit the form

### Viewing Statistics

- **Home Page**: See recent matches
- **Players**: View a list of all players and their profiles
- **Leaderboard**: Check the ranking of players based on win percentage
- **Player Profile**: Click on a player's name to see their detailed statistics and match history

## Development

### Project Structure

```
table_football_app/
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker configuration
├── Makefile                # Make commands for common operations
├── requirements.txt        # Python dependencies
├── pytest.ini              # Pytest configuration
├── manage.py               # Django management script
├── table_football/         # Django project settings
│   ├── settings.py         # Main settings file
│   ├── test_settings.py    # Test-specific settings
│   ├── urls.py             # Main URL routing
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── scores/                 # Django app for match tracking
│   ├── models.py           # Data models
│   ├── views.py            # View controllers
│   ├── urls.py             # URL routing for the app
│   ├── forms.py            # Form definitions
│   ├── admin.py            # Admin interface configuration
│   ├── signals.py          # Django signals for model events
│   ├── tests/              # Test directory
│   ├── templates/          # HTML templates
│   └── static/             # App-specific static files
├── templates/              # Project-wide HTML templates
└── static/                 # Static files (CSS, JS, images)
```

### Technology Stack

- **Backend**: Django 4.2.10, Python 3.11
- **Database**: PostgreSQL (production), SQLite (development/testing)
- **Authentication**: Google OAuth via django-allauth
- **Frontend**: Bootstrap 5, CSS animations, JavaScript
- **Testing**: pytest, pytest-django, pytest-cov
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose

### Database Schema

- **Player**: Linked to User model, with nickname and profile color
- **Match**: Records match details, scores, and players
- **PlayerStats**: Tracks statistics for each player

### Running Tests

The project uses pytest for testing with comprehensive test coverage:

```bash
# Run tests using make
make test

# Run tests directly with pytest
docker-compose exec web pytest -v

# Run tests with coverage report
docker-compose exec web pytest --cov=. --cov-report=term
```

#### Testing Features

- **Isolated Test Environment**: Tests run with an in-memory SQLite database
- **Comprehensive Coverage**: 84% code coverage across the application
- **CI/CD Integration**: Automated testing via GitHub Actions
- **Signal Handling**: Properly isolated signal processing during tests
- **Static Files**: Configured for proper handling during tests

#### Test Structure

```
scores/tests/
├── conftest.py             # Pytest fixtures and configuration
├── test_models.py          # Tests for data models
├── test_views.py           # Tests for views and templates
└── test_urls.py            # Tests for URL routing
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Run tests to ensure everything works**
   ```bash
   make test
   ```
5. **Submit a pull request**

### Development Workflow

1. **Set up the development environment**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd table_football_app
   
   # Create .env file with required variables
   cp .env.example .env
   
   # Build and start the containers
   docker-compose up --build
   ```

2. **Make code changes**
   - Follow Django's coding style
   - Add tests for new features
   - Update documentation as needed

3. **Run tests**
   ```bash
   make test
   ```

4. **Check code coverage**
   ```bash
   make coverage
   ```

5. **Format code**
   ```bash
   make lint
   ```

### Common Make Commands

The project includes a Makefile with common commands:

```bash
# Help
make help              # Show help message with all available commands

# Docker commands
make docker-build      # Build Docker containers
make docker-up         # Start Docker containers
make docker-down       # Stop Docker containers
make logs              # View Docker logs

# Development
make runserver         # Run development server
make shell             # Open Django shell
make clean             # Remove Python compiled files

# Database operations
make makemigrations    # Create database migrations
make migrate           # Apply database migrations
make createsuperuser   # Create a superuser

# Static files
make collectstatic     # Collect static files

# Testing
make test              # Run all tests with pytest
make test-urls         # Run only URL tests
```

## Deployment

For production deployment, make sure to:

1. Set `DEBUG=False` in your `.env` file
2. Generate a strong random `SECRET_KEY`
3. Configure proper database settings
4. Set up proper email settings
5. Update Google OAuth redirect URIs for your production domain
6. Consider using a production-ready web server like Nginx

## License

[MIT License](LICENSE)

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Animate.css](https://animate.style/)
- [Font Awesome](https://fontawesome.com/)
