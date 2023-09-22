# Microblog

Microblog is a simple web application built with Flask that allows users to share their thoughts, ideas, and experiences with a vibrant community. It provides a platform for open discussions, creative expression, and the exchange of diverse viewpoints.

## Features

- **User Authentication**: Secure user registration and login system.
- **Profile Management**: Users can update their profiles and upload avatars.
- **Post Creation**: Easy-to-use interface for creating and publishing posts.
- **Commenting**: Engage in discussions by commenting on posts.
- **Following**: Follow other users and view their posts on your timeline.
- **Explore**: Discover new content and users in the Explore section.
- **Email Notifications**: Receive email notifications for important activities.
- **Responsive Design**: User-friendly experience across different devices.

## Technologies Used

- **Flask**: A micro web framework for Python.
- **SQLAlchemy**: A powerful and flexible Object Relational Mapper (ORM).
- **SQLite**: Lightweight, serverless, and self-contained database.
- **Bootstrap**: Front-end framework for responsive and attractive UI.
- **Flask-Mail**: Extension for email handling.
- **Flask-Login**: User session management.
- **Flask-WTF**: Integration with WTForms for forms handling.

## Getting Started

1. Clone the repository:

   ```shell
   git clone https://github.com/m-rakesh-kr/flask_microblog.git
   cd flask_microblog
   ```

2. Create a virtual environment:

   ```shell
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up environment variables (see Configuration section).

5. Initialize the database:

   ```shell
   flask db upgrade
   ```

6. Run the application:

   ```shell
   flask run
   ```

7. Access the app in your web browser at `http://localhost:5000`.

## Configuration

Create a `.env` file in the project root directory and add the following configuration:

```env
SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///your_database.db
MAIL_SERVER=smtp.yourmailserver.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your@email.com
MAIL_PASSWORD=your_email_password

BROKER_URL_CELERY = ''
BACKEND_URL_CELERY = ''

#configuration for Social Auth
GOOGLE_CLIENT_ID = ""
GOOGLE_CLIENT_SECRET = ""
```

## Contributing

We welcome contributions from the community! If you find a bug or have a feature request, please open an issue. Pull requests are also encouraged.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

