# 🎓 College Digital Complaint Box

A complete digital complaint management system designed for colleges, built with Flask, SQLite, and modern web technologies. This platform enables students to submit, track, and manage complaints while administrators can efficiently review and resolve them.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

### 👨‍🎓 For Students
- **User Registration & Login** - Secure authentication with hashed passwords
- **Submit Complaints** - File complaints under various categories
- **Track Complaints** - Monitor the status of submitted complaints
- **Edit Complaints** - Modify pending complaints before they're processed
- **View History** - Access all previously submitted complaints

### 👨‍💼 For Administrators
- **Admin Dashboard** - Centralized management panel
- **View All Complaints** - Access complaints from all users
- **Update Status** - Change complaint status (Pending → In Progress → Resolved)
- **Statistics & Analytics** - View complaint trends and category breakdowns
- **Monthly Reports** - Track complaint patterns over time

### 🏷️ Complaint Categories
- 🏠 Hostel
- 📚 Academics
- 🏗️ Infrastructure
- 🍽️ Mess/Canteen
- 🏛️ Administration
- 📋 Other

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python Flask 3.0.3 |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Templating | Jinja2 |
| Authentication | Flask Sessions + Werkzeug |
| CORS | Flask-CORS |
| Production Server | Gunicorn |
| Containerization | Docker |

---

## 📁 Project Structure

```
SEMPROJECT/
├── run.py                    # Application entry point
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── complaint_box.db          # SQLite database
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose config
├── railway.json              # Railway deployment config
│
└── app/
    ├── __init__.py           # Flask app factory
    ├── db.py                 # Database utilities
    │
    ├── routes/
    │   ├── main.py           # Page routes
    │   ├── auth.py           # Authentication APIs
    │   ├── complaints.py     # Complaint management APIs
    │   └── admin.py          # Admin APIs
    │
    ├── templates/            # HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── login.html
    │   ├── signup.html
    │   ├── submit.html
    │   ├── track.html
    │   ├── my_complaints.html
    │   ├── admin_login.html
    │   └── admin_dashboard.html
    │
    └── static/
        ├── css/              # Stylesheets
        └── js/               # JavaScript files
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/college-complaint-box.git
   cd college-complaint-box
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open in browser**
   ```
   http://localhost:8000
   ```

---

## 🐳 Docker Deployment

### Using Docker Compose
```bash
docker-compose up --build
```

### Using Docker directly
```bash
docker build -t complaint-box .
docker run -p 8000:8000 complaint-box
```

---

## 🔑 Default Credentials

### Admin Account
| Username | Password |
|----------|----------|
| `admin` | `admin123` |

> ⚠️ **Important**: Change the default admin password in production!

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/signup` | Register new user |
| POST | `/api/login` | User/Admin login |
| POST | `/api/logout` | Logout |

### Complaints (User)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/submit_complaint` | Submit new complaint |
| GET | `/api/track_complaint?id=X` | Track complaint by ID |
| GET | `/api/user_complaints` | Get user's complaints |
| PUT | `/api/edit_complaint` | Edit pending complaint |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admin/login` | Admin login |
| GET | `/api/admin/complaints` | Get all complaints |
| PUT | `/api/admin/complaints/update_status` | Update complaint status |
| GET | `/api/admin/stats` | Get statistics |

---

## 🗃️ Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| user_id | INTEGER | Primary Key |
| name | TEXT | Full name |
| email | TEXT | Unique email |
| username | TEXT | Unique username |
| password_hash | TEXT | Hashed password |

### Admins Table
| Column | Type | Description |
|--------|------|-------------|
| admin_id | INTEGER | Primary Key |
| username | TEXT | Unique username |
| password_hash | TEXT | Hashed password |

### Complaints Table
| Column | Type | Description |
|--------|------|-------------|
| complaint_id | INTEGER | Primary Key |
| user_id | INTEGER | Foreign Key (users) |
| complaint_text | TEXT | Complaint description |
| category | TEXT | Category type |
| status | TEXT | Pending/In Progress/Resolved |
| submitted_at | TEXT | Creation timestamp |
| updated_at | TEXT | Last update timestamp |

---

## 📊 Complaint Status Flow

```
┌─────────┐     ┌─────────────┐     ┌──────────┐
│ Pending │ ──► │ In Progress │ ──► │ Resolved │
└─────────┘     └─────────────┘     └──────────┘
```

> **Note**: Once a complaint moves forward, it cannot be reverted to a previous status.

---

## 🔒 Security Features

- ✅ Password hashing using Werkzeug
- ✅ Session-based authentication
- ✅ Protected API routes with decorators
- ✅ Input validation and sanitization
- ✅ CORS configuration for cross-origin requests

---

## 🚢 Deployment

### Railway
The project includes `railway.json` for easy deployment on Railway:
```bash
railway up
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Your Name** - *Initial work*

---

## 🙏 Acknowledgments

- Flask documentation and community
- SQLite for providing a lightweight database solution
- All contributors and testers

---

<p align="center">
  Made with ❤️ for College Students
</p>
