# E-Shop Flask Application

A modern e-commerce web application built with Flask, featuring user authentication, product management, shopping cart functionality, and order processing.

## Features

- User authentication (register, login, logout)
- Product browsing and categorization
- Shopping cart functionality
- Checkout process with shipping options
- Order management
- User profile and settings
- Responsive design using Bootstrap

## Tech Stack

- Python 3.8+
- Flask
- SQLAlchemy
- Flask-Login
- Bootstrap 5
- SQLite (development)

## Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd eshop
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:8080`

## Deployment

### Vercel Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy to Vercel:
```bash
vercel
```

3. Set up environment variables in Vercel:
- `SECRET_KEY`: Your secret key for Flask sessions
- `DATABASE_URL`: Your database URL (if using a different database)

## Environment Variables

- `SECRET_KEY`: Secret key for Flask sessions
- `DATABASE_URL`: Database URL (defaults to SQLite)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 