CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT UNIQUE,
        content TEXT,
        summary TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    , job_id INTEGER);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        source_name TEXT,
        source_url TEXT,
        FOREIGN KEY(article_id)
        REFERENCES articles(id)
    );
CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        description TEXT
    );
CREATE TABLE keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER,
        keyword TEXT,
        FOREIGN KEY(article_id)
        REFERENCES articles(id)
    );
CREATE TABLE jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
CREATE TABLE logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
CREATE TABLE knowledge_articles
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    title TEXT,
    summary TEXT,
    content TEXT,
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
, job_id INTEGER);
CREATE TABLE knowledge_sources
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    knowledge_id INTEGER,

    title TEXT,

    url TEXT,

    domain TEXT,

    quality_score INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
, job_id INTEGER);
