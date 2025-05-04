# DirecMex

DirecMex is a simple web application built with Flask and PostgreSQL that allows users to search for location details (such as neighborhood, city, municipality, and state) by entering a 5-digit ZIP code.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#how-to-use-this-project)
- [Requirements](#requirements)
- [Contribution](#contribution)
- [Learn More](#learn-more)

---

## Project Structure

```
direcmex/
├── src/
│   ├── app.py              # Flask main application
│   ├── templates/
│   │   └── index.html      # HTML frontend form
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Features

- Simple web form to input ZIP codes.
- PostgreSQL query to retrieve detailed address info.
- Data normalized by neighborhood, municipality, city, and state.
- Lightweight Flask application.
- Basic error handling for invalid or unregistered ZIP codes.

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/LSCasas/direcmex.git
   cd direcmex/src
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r ../requirements.txt
   ```

4. **Run the server:**

   ```bash
   python app.py
   ```

---

## How to Use This Project

1. Start the Flask development server.
2. Open your browser and go to:

```
http://localhost:5000
```

3. Enter a 5-digit ZIP code in the input field and submit the form.
4. The system will query the database and return the following information:

- Colonias (neighborhoods)
- Municipio (municipality)
- Ciudad (city)
- Estado (state)

---

## ZIP Code Lookup Example

When a valid ZIP code is submitted (e.g., `50000`), the app will perform the following query:

```sql
SELECT c.descripcion AS colonia, m.descripcion AS municipio,
       ci.descripcion AS ciudad, e.descripcion AS estado
FROM cp cp
JOIN colonias c ON cp.id_colonia = c.id_colonia
JOIN municipios m ON c.id_municipio = m.id_municipio AND c.id_estado = m.id_estado
JOIN ciudades ci ON ci.id_municipio = m.id_municipio AND ci.id_estado = m.id_estado
JOIN estados e ON e.id_estado = m.id_estado
WHERE cp.cp = %s
```

If found, you’ll get results like:

```json
{
  "colonias": ["Centro", "Del Valle", "San Pedro"],
  "municipio": "Toluca",
  "ciudad": "Toluca de Lerdo",
  "estado": "Estado de México"
}
```

If not found, the system will display:

```
No se encontró información para ese C.P.
```

---

## Requirements

- Python 3.x
- PostgreSQL
- Flask == 3.1.0
- psycopg2-binary == 2.9.10

---

## Contribution

If you want to contribute to this project:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Make your changes and commit:

   ```bash
   git commit -am 'Add new feature'
   ```

4. Push to your fork:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a Pull Request.

---

## Learn More

- [Flask Documentation](https://flask.palletsprojects.com/) – Web framework used in this project.
- [PostgreSQL Documentation](https://www.postgresql.org/docs/) – SQL database used for storing location data.

Your feedback and suggestions are always welcome!
