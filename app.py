

from flask import Flask, request, render_template
from scriptFin import reccomndation
app = Flask(__name__)
def get_data():
    data = []
    from pymongo import MongoClient
    client = MongoClient(
            "mongodb+srv://Hassaan149:random098123@user-credentials.qgy2m.mongodb.net/UserDB?retryWrites=true&w=majority")
    db = client["UserDB"]
    collection = db["REs"]
    results = collection.find({})
    for result in results:
       data.append(result)
    return data

def recc(Budget, Est, Type):
    from pandas import DataFrame
    from sklearn.ensemble import RandomForestClassifier
    data = DataFrame(get_data())
    data.drop(['_id'], axis=1)
    from sklearn.preprocessing import LabelEncoder
    leApph = LabelEncoder().fit_transform(data.APPH)
    leStime = LabelEncoder().fit_transform(data.S_time)
    leGen = LabelEncoder().fit_transform(data.genre)
    LeTarget = LabelEncoder().fit_transform(data.grade)
    pph = {1500: 2, 1000: 1, 500: 0}
    est = {20: 0, 30: 1, 50: 2}
    grade = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
    LEdataframe = DataFrame(leApph, columns=['Apph'])
    LEdataframe['Stime'] = leStime
    LEdataframe['genre'] = leGen
    LEdataframe['Grade'] = LeTarget
    LeX = LEdataframe.drop(
    LEdataframe[['Grade', 'genre']], axis=1)
    LeY = LeTarget
    model = RandomForestClassifier(n_estimators=50, criterion='gini')
    model.fit(LeX, LeY)
    pred = grade.get(model.predict([[pph.get(Budget), est.get(Est)]])[0])
    recc = data.loc[(data['grade'] == pred) & (
    data['genre'] == Type)].head(5)
    return recc.Names


@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        
        data = list(recc(int(request.form.get("price")), int(
            request.form.get("service")), request.form.get("genre")))
        return render_template('reccommend.html', data=data)

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
