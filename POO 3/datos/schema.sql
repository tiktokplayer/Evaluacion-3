DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    userId INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
) AUTO_INCREMENT = 101;

CREATE TABLE comments (
    id INT NOT NULL AUTO_INCREMENT,
    post_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

CREATE INDEX idx_posts_userId ON posts(userId);
CREATE INDEX idx_posts_created_at ON posts(created_at);
CREATE INDEX idx_comments_postId ON comments(post_id);
CREATE INDEX idx_comments_email ON comments(email);
CREATE INDEX idx_comments_created_at ON comments(created_at);

INSERT INTO posts (id, title, body, userId) VALUES (100, 'Reserved', 'Reserved for sequence', 1);
DELETE FROM posts WHERE id = 100;