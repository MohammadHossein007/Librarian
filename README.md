# 📚 Django Library Management System

A robust web-based Library Management System built using the Django framework. This system is designed to allow members to browse and borrow books, and librarians to manage the library’s resources effectively.

## 🚀 Features

### For Members
- Multi-step registration with email verification
- Complete profile after email confirmation
- User dashboard to track borrowed books and manage wishlist
- Book detail pages with rating and review functionality

### For Librarians
- Admin panel to manage:
  - Books and their categories
  - Authors and members
  - Loans and returns
- Book availability status
- Manual or automated return dates


## 🛠️ Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, Tailwind CSS
- **Database:** SQLite (default for development)


## 🔧 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone (https://github.com/MohammadHossein007/Librarian)
   cd librarian
   
2. **Create and activate virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies
    pip install -r requirements.txt

4. Apply migrations
    python manage.py migrate

5. Run the server
   python manage.py runserver
