# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
# ]
# ///

import csv
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS: kisi bhi website ko GET request bhejne do
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

# CSV ko ek baar padho, jab server start ho
students = []
csv_path = Path(__file__).parent / "q-fastapi.csv"
with open(csv_path, newline="", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        students.append({"studentId": int(row["studentId"]), "class": row["class"]})


@app.get("/api")
async def get_students(class_: list[str] | None = Query(default=None, alias="class")):
    if class_:
        result = [s for s in students if s["class"] in class_]
    else:
        result = students
    return {"students": result}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
