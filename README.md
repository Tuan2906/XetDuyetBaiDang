

# Post Review Website

## Overview
This project involves building a post review website where posts are reviewed and managed. The system includes backend and frontend components to handle post moderation, user notifications, and authentication.

## Backend
The backend is responsible for the following functionalities:
- **Check Sensitive Words:** Using AI to detect sensitive words in posts.
- **Update Post Status:** API endpoints to update the status of posts.
- **Send Notification Emails:** Notify users when their posts are reviewed.
- **Authentication & Authorization:** Login functionality with employee roles and permissions.

**Technology Used:** Python (Django Rest Framework)

## Frontend
The frontend provides the following features:
- **Post Review Interface:** Interface for automatic AI checks, rejecting posts, approving posts, and viewing post details.
- **Login Interface:** Allows users to log in to the system.

**Technology Used:** ReactJS

## Installation

### Backend
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/post-review-backend.git
   ```
2. Navigate to the backend directory:
   ```bash
   cd post-review-backend
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/post-review-frontend.git
   ```
2. Navigate to the frontend directory:
   ```bash
   cd post-review-frontend
   ```
3. Install the required packages:
   ```bash
   npm install
   ```
4. Start the development server:
   ```bash
   npm start
   ```

## Usage

- **Backend API:** The backend provides RESTful APIs for managing posts, sensitive word checking, and user notifications.
- **Frontend:** The frontend offers a user-friendly interface for post review and login functionalities.

## Contributing
Feel free to fork the repository and submit pull requests. Contributions are welcome!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


