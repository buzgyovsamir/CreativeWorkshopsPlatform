# Creative Workshops Platform

A full-featured Django web application for organizing, discovering, and booking creative workshops.

---


Creative Workshops Platform allows users to:
- Explore creative workshops (public section)
- Register and manage their profile
- Book workshops and leave reviews
- Organize and manage their own workshops

The project demonstrates advanced Django concepts including CBVs, REST APIs, Celery, and PostgreSQL integration.

---


- User registration
- Login / Logout
- Extended user model (Profile)

- Organizers
- Participants
- Access control based on ownership and roles

- Create / Edit / Delete workshops (organizers only)
- Browse all workshops
- View workshop details
- Filter and categorize workshops

- Book a workshop
- Prevent duplicate bookings
- Cancel booking

- Create / Edit / Delete reviews
- One review per user per workshop

- Booking confirmation email (async)

- Workshops API
- Reviews API

---


- Django 6
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Bootstrap 5
- Gunicorn
- WhiteNoise

---


- `accounts` → users & authentication
- `workshops` → workshop logic
- `bookings` → booking system
- `reviews` → reviews system
- `common` → shared logic

---

## ⚙️ Setup (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/buzgyovsamir/CreativeWorkshopsPlatform.git
cd CreativeWorkshopsPlatform
