import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
global count_connection=0

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    count_connection+=1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post
def count_db_connection():
    if:
# Define the Flask application
app = Flask(__name__) #这边是创建一个flask的应用实例,name的作用主要是确定应用的根目录
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application  这边是显示所有的文章
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.warning(f'sorry for the article or this post cannot be found') #要注意的是,这边的info的命令,或者说info的指令是用来给记录一般信息或者系统变化的,而warning是用来记录可能的问题或者异常情况的
      return render_template('404.html'), 404
    else:
        app.logger.info(f'you have got the article thank you very much')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info(f'you have got the information about our platform')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f'New article created: {title}')
            return redirect(url_for('index'))

    return render_template('create.html')
#define the health reaction 
@app.route('/health')
def health():
    try:
        connection=get_db_connection()
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM posts')
        connection.close()
        response={'result':'OK - healthy'}
        return jsonify(response),200;
     except Exception as e:
        return jsonify({'error':str(e)}),500

#define the metrics reaction ,连接数和psot数,都是非常重要的指标,当发布文章或者留下评论时,都会连接到数据库,连接数能帮助我们有效评估连接的数量,其次post数量则表示的是数据库,或者说平台上的文章的数量
@app.route('/metrics')
def metrics():
    connection=get_db_connection()
    posts=connection.execute('SELECT*FROM posts').fetchall()
    connection.close()
    posts_count=len(posts)
    data={'db_connection_count':count_connection,'post_count':posts_count}
    return data
    
    
 #Function that logs messages
def log_message(msg):
    app.logger.info('{time} | {message}'.format(
        time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), message=msg))   

@app.route('/debug_logs')
def debug_logs():
    app.logger.debug("Debugging message: This is a DEBUG level log.")
    return "Check logs for DEBUG messages"
    
# start the application on port 3111
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
   app.run(host='0.0.0.0', port='3111')
