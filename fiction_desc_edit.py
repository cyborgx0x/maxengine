from app.models import Fiction, Author, Chapter
from app import db
from datetime import datetime
import json

fics = Fiction.query.all()
for fic in fics:
    text = fic.desc
    blocks = []
    x = text.split('</p><p>')
    for n in x:
        k = n.split("\n")
        
        for y in k:
            block = {
                "type": "paragraph",
                "data": {
                "text": y
                }
            }
            blocks.append(block)
    # print(blocks)
        
    now = datetime.now()
    new_desc = {
        "time": datetime.timestamp(now),
        "blocks": blocks,
        "version": "2.8.1"
    }
    print("done crack")
    fic.desc = json.dumps(new_desc)
    # print(type(fic.desc))
    db.session.commit()