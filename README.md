# 🎬 Booking System: Tastypie Leaning Path

**Welcome to my Cinema Booking System!** 🌟 This project is a web application built using **Django** and **Tastypie**, providing a RESTful API for managing users, profiles, rooms, sessions, and seats for a cinema booking system.

This project uses **Python 2.7**, **Django 1.11.29**, and **Tastypie 0.14.1** because these were requirements for my current back-end job. **Docker** was used for local development since Python 2 is no longer shipped or supported. 🐳

If you are somehow running this on your host machine, you may want to use a **virtualenv**. 🐍

## ✨ Features

- 👤 User and Profile Management
- 🏛️ Room and Session Management
- 🎟️ Seat Reservation System
- 🔗 RESTful API using Tastypie

## 📋 Requirements

- **Python 2.7**
- **Docker** (optional)

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/userexample.git
   cd userexample
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Application

### Using Python

1. Make sure you have the required Python packages installed.

2. Apply the migrations:
   ```bash
   python manage.py migrate
   ```

3. Start the development server:
   ```bash
   python manage.py runserver
   ```

4. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 🌐. (Although there is nothing to see there lol 😅)

### Using Docker

⚠️ This Dockerfile.dev is used for local development, it does not provide a full ready-to-use application. You may install and run the application. Follow the steps below:

1. Build the Docker image:
   ```bash
   docker build -f Dockerfile.dev -t python2-tastypie:dev .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 -v .:/workspace -dt python2-tastypie:dev
   ```
   Here we forward the port 8000 to the container, mount the current working directory to the container and make it run in the background.

3. Attach your IDE to the running container (you may use VSCode or any other IDE).
   There is a plugin for Docker that allows you to attach to a running container while using VSCode.

4. Open your terminal inside your IDE or using docker exec:
   ```
   docker exec -it python2 /bin/sh
   ```

5. Apply the migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 🌐.

## 🧪 Testing

Run the tests using Django's test framework:
```bash
python manage.py test
```

## 🤝 Contributing

We welcome contributions! 🎉 Please fork the repository and submit a pull request with your changes.

## 📝 License

This project is licensed under the **MIT License**. 

Feel free to explore, modify, and enhance the User Example Project. If you encounter any issues or have any questions, don't hesitate to reach out! 

Happy coding! 💻✨
