# TJCampusLinker

A campus social networking and activity management platform designed to help students discover, create, and participate in campus activities.

## 🚀 Features

- **User Management**: Registration, login, password recovery, and profile management
- **Activity Management**: Create, search, and browse campus activities
- **Team Management**: Organize and manage activity teams
- **Real-time Chat**: Group chat and personal messaging
- **Activity Search**: Filter activities by class, campus, and other criteria
- **Admin Panel**: Administrative interface for managing activities and users

## 🛠️ Tech Stack

### Backend
- Django 5.1.2
- Django REST Framework
- MySQL

### Frontend
- Vue 3 with TypeScript
- Vite
- Vuetify 3
- Element Plus
- Vue Router

## 📁 Project Structure

```
tjcampuslinker/
├── BackEnd/
│   └── TJLinker/
│       ├── accounts/          # User authentication and management
│       ├── lists/             # Activity and list management
│       └── TJLinker/          # Django project settings
└── FrontEnd/
    └── src/
        ├── pages/             # Vue pages
        ├── components/        # Reusable Vue components
        └── router/            # Vue Router configuration
```

## 🏃 Quick Start

### Prerequisites

- Python 3.x
- Node.js 16+
- MySQL 8.0+

### Backend Setup

1. Navigate to the backend directory:
```bash
cd BackEnd/TJLinker
```

2. Install Python dependencies:
```bash
pip install django djangorestframework django-cors-headers mysqlclient
```

3. Configure MySQL database in `TJLinker/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tjlinker',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py populate_class_table
```

5. Start the development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd FrontEnd
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

## 📝 Available Scripts

### Frontend
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint and fix code

## 🔧 Configuration

- Backend API runs on `http://localhost:8000`
- Frontend runs on `http://localhost:5173` (default Vite port)
- CORS is enabled for all origins in development mode

## 📄 License

This project is part of a course assignment.
