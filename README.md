# 📚 Course Search and Recommendation Engine using Elasticsearch and Django

In today's digital learning landscape, users expect fast, intelligent, and typo-tolerant search experiences when exploring online courses. This project demonstrates how to build a robust course search and recommendation engine using **Elasticsearch**, **Django**, and **MySQL**.

---

## 🚀 Features

- 🔍 Full-text and fuzzy search
- ✨ Autocomplete & semantic search (vector embeddings)
- ✅ Boolean and proximity search
- 🤖 Course recommendations using collaborative & content-based filtering
- 🐳 Docker-based Elasticsearch and MySQL setup
- 📊 Optional integration with Kibana for query visualization

---

## 🧠 Techniques Covered

| Technique           | Description |
|---------------------|-------------|
| **Fuzzy Search**    | Handles typos and near matches (e.g., `"pyton"` returns Python courses) |
| **Full-Text Search**| Matches content across title, description, etc. |
| **Boolean Queries** | Combine filters like `AND`, `OR`, `NOT` for precise results |
| **Proximity Search**| Find words that appear near each other |
| **Vector Search**   | Semantic matching using NLP embeddings |
| **Recommendations**| Based on user behavior or similar content |

---

## 📦 Tech Stack

- **Backend**: Django (Python)
- **Search Engine**: Elasticsearch 9.0.0
- **Database**: MySQL
- **Optional**: Kibana for visualizing Elasticsearch data
- **Containerization**: Docker

---

## 🐳 Docker Setup

### 1. Run Elasticsearch

```bash
docker network create elastic

docker pull docker.elastic.co/elasticsearch/elasticsearch-wolfi:9.0.0

docker run -d --name my-elasticsearch-container \
  --network elastic \
  -p 9200:9200 \
  -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch-wolfi:9.0.0
```

### 2. Start MySQL Container

```bash
docker run --name mysql-course-db \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=courses_db \
  -e MYSQL_USER=user \
  -e MYSQL_PASSWORD=password \
  -p 3306:3306 \
  -d mysql:latest
```

## 💾 Database Initialization

### 1. Connect to MySQL

```bash
docker exec -it mysql-course-db mysql -u root -p
```

### 2. Create courses Table

```bash
USE courses_db;

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INT,
    sub_category_id INT,
    language VARCHAR(50),
    source VARCHAR(50),
    level VARCHAR(50),
    is_valid BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🐍 Run Django Backend

### 1. Clone the Repository

```bash
git clone https://github.com/wynnteo/elasticsearch_course_search.git
cd elasticsearch_course_search
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Indexing Data into Elasticsearch

```bash
python manage.py index_courses
```

## 📖 Learn More

For a step-by-step explanation and deeper insights into the implementation, please refer to the full tutorial:

👉 [Creating a Powerful Course Search and Recommendation Using Elasticsearch I](https://your-blog-link.com)

The post covers everything from Elasticsearch basics to building intelligent course recommendations with Django.

### 6. Run the Development Server

```bash
python manage.py runserver
```


