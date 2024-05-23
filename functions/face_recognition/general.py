import sqlite3
import pickle
import cv2
from deepface.DeepFace import represent, verify

# Connect to the SQLite database (or create it if it doesn't exist)
def get_embedding(image_path, target_size=(224,224), model_name="GhostFaceNet"):
  img = cv2.imread(image_path)
  img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
  img = cv2.resize(img,target_size, interpolation=cv2.INTER_NEAREST)
  embedding_objs = DeepFace.represent(
  img_path = img,
  model_name = model_name,
)
  if isinstance(embedding_objs,type(None)):
    return None
  else:
    return embedding_objs[0]['embedding']

def compare(emb_01,emb_02,model_name="GhostFaceNet"):
  result = DeepFace.verify(
    img1_path = emb_01,
    img2_path = emb_02,
    model_name = model_name,
    silent=True,
  )
  return result
def create_embedding_db():
  conn = sqlite3.connect('embeddings.db')
  cursor = conn.cursor()

  # Create a table to store the embeddings with a name column
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS embeddings (
      id INTEGER PRIMARY KEY,
      name TEXT,
      embedding BLOB
  )
  ''')

  # Commit the changes and close the connection
  conn.commit()
  conn.close()

def create_embedding_record(embedding, name, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Serialize the embedding
    serialized_embedding = pickle.dumps(embedding)

    # Insert the name and serialized embedding into the table
    cursor.execute('''
    INSERT INTO embeddings (name, embedding) VALUES (?, ?)
    ''', (name, serialized_embedding))

    # Commit the changes
    conn.commit()
    conn.close()

def retrieve_embedding_records(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT name, embedding FROM embeddings')
    rows = cursor.fetchall()
    data = []
    for row in rows:
        name = row[0]
        serialized_embedding = row[1]
        embedding = pickle.loads(serialized_embedding)
        data.append((name, embedding))
    conn.close()
    return data

def verify_face_in_db(image_path, db_path):
    unkown_face_emb = get_embedding(image_path)
    emb_data = retrieve_embedding_records(db_path)
    verified_faces_names = []
    if unkown_face_emb != None:
      for _, (name, emb) in enumerate(emb_data):
        result = compare(unkown_face_emb, emb)
        if result['verified']:
          verified_faces_names.append(name)
    return verified_faces_names
