# 🎓 College Digital Complaint Box

A comprehensive digital complaint management system designed for colleges, built with Flask, SQLite, and modern web technologies. This full-stack web application allows students to submit, track, and manage complaints while providing administrators with powerful dashboard analytics.

![College Complaint Box](https://img.shields.io/badge/Status-Complete-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey) ![SQLite](https://img.shields.io/badge/SQLite-3-green)

## ✨ Features

### 👨‍🎓 Student Features
- **User Registration & Authentication** - Secure signup and login system
- **Complaint Submission** - Submit complaints with college-specific categories
- **Complaint Tracking** - Track status of submitted complaints by ID
- **Edit Pending Complaints** - Modify complaints that haven't been processed yet
- **My Complaints Dashboard** - View all personal complaints with status indicators
- **Responsive Design** - Works seamlessly on desktop and mobile devices

### 👨‍💼 Admin Features
- **Admin Authentication** - Secure admin login system
- **Complaint Management** - View and update complaint statuses
- **Analytics Dashboard** - Charts showing complaint statistics and trends
- **Status Updates** - Change complaint status (Pending → In Progress → Resolved)
- **Category Analytics** - Breakdown of complaints by category
- **Monthly Trends** - Track complaint patterns over time

### 🎨 UI/UX Features
- **Modern Dark Theme** - Sleek, professional interface
- **Smooth Animations** - Welcome messages, loading spinners, success animations
- **Interactive Charts** - Visual data representation using Chart.js
- **Real-time Updates** - Dynamic status changes and form validation
- **Accessibility** - Proper contrast and keyboard navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Girish3012-AD/college-complaint-box.git
   cd college-complaint-box
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to: `http://localhost:5000`
   - Or on network: `http://192.168.1.10:5000` (your local IP)

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access at**: `http://localhost:5000`

## 🔐 Default Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `admin123`

*⚠️ Change these credentials in production!*

## 📁 Project Structure

```
college-complaint-box/
├── app.py                 # Flask application & API endpoints
├── requirements.txt       # Python dependencies
├── schema.sql           # Database schema
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Docker Compose setup
├── styles.css           # Global CSS styles & animations
├── .gitignore           # Git ignore rules
├── README.md            # Project documentation
│
├── HTML Templates/
│   ├── index.html        # Home page with navigation
│   ├── login.html        # User login page
│   ├── signup.html       # User registration
│   ├── submit.html       # Complaint submission form
│   ├── track.html        # Complaint tracking page
│   ├── my_complaints.html # User's complaint dashboard
│   ├── admin_login.html  # Admin authentication
│   └── admin_dashboard.html # Admin management interface
│
└── JavaScript/
    ├── submit.js         # Complaint submission logic
    ├── track.js          # Complaint tracking functionality
    ├── admin_login.js    # Admin login with animations
    └── admin_dashboard.js # Dashboard charts & management
```

## 🗄️ Database Schema

The application uses SQLite with the following tables:

- **users** - Student accounts (id, name, email, username, password_hash)
- **admins** - Administrator accounts (id, username, password_hash)
- **complaints** - Complaint records (id, user_id, text, category, status, timestamps)

## 🎯 Complaint Categories

- **Academic** - Course content, grades, examinations
- **Facilities** - Infrastructure, maintenance, amenities
- **Administration** - Policies, procedures, staff
- **Library** - Books, resources, services
- **Hostel** - Accommodation, facilities, rules
- **Other** - Miscellaneous complaints

## 📊 Status Workflow

1. **Pending** - Initial submission state
2. **In Progress** - Being reviewed/processed
3. **Resolved** - Issue resolved/completed

## 🌐 Deployment Options

### Railway (Free & Recommended)
1. Connect your GitHub repository
2. Automatic deployment on code push
3. Built-in database support

### Vercel
1. Import from GitHub
2. Add `vercel.json` configuration
3. Serverless deployment

### Heroku
1. Create Heroku app
2. Connect GitHub repository
3. Automatic deploys

### Local Network Access
- Run `python app.py` with `host='0.0.0.0'`
- Access from any device on your network

## 🛠️ Technologies Used

### Backend
- **Flask** - Python web framework
- **SQLite** - Lightweight database
- **Werkzeug** - Password hashing & security
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualization

### DevOps
- **Docker** - Containerization
- **Git** - Version control
- **GitHub** - Code hosting & collaboration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for college assignment requirements
- Inspired by modern complaint management systems
- Uses open-source libraries and frameworks

## 📞 Support

For questions or issues:
- Check the [Issues](https://github.com/Girish3012-AD/college-complaint-box/issues) page
- Review the code documentation
- Test locally with the provided setup instructions

---

**⭐ Star this repository if you find it helpful!**

*Developed with ❤️ for educational purposes*