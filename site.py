from flask import Flask, render_template,url_for,redirect,request
from flask.helpers import flash
from pymongo import MongoClient


app = Flask(__name__)
app.config['SECRET_KEY'] = "saucisse"
client = MongoClient("mongodb+srv://saucisse:saucisse@cluster0.wedwq.mongodb.net/?retryWrites=true&w=majority")

def connexion(parametre):

    db = parametre.cancer
    don = db.donation

    return don

def fermer_connexion(client):

    client.close()
 
@app.route('/')
def site():
    return render_template("site.html")


@app.route('/formulaire', methods=('GET', 'POST'))
def formulaire():
    
    acces = connexion(client)

    if request.method == "POST":
        
        nom = request.form["user_nom"]
        prenom = request.values.get("user_prenom")
        mail = request.values.get("user_mail")
        montant = request.values.get("user_montant")
        messsage = request.values.get("user_message")
   
        recup = {"nom":nom,"prenom":prenom,"mail":mail,"montant":montant,"message":messsage}
        
        acces.insert_one(recup)

        fermer_connexion(client)

        flash("Promesse de don enregistrée,nous vous remercions")

        return redirect(url_for('site'))

         
    
    return render_template('formulaire.html')


@app.route('/resultat')
def resultat():

    total = total_don()
    acces = connexion(client)

    resultats =  acces.find({},{"_id":0})
    #resultats = list(resultats)

    fermer_connexion(client)

    return render_template("resultats.html",resultats=resultats,total = total)


    

def total_don():

        acces = connexion(client)
        dons = acces.find({},{"_id":0})
        total = 0

        for i in dons:

            for j in i.keys():
                
                if j =="montant":
                    
                    montant = i["montant"]
                    total = int(montant) + total 
                  
                
        fermer_connexion(client)

        return total


    
if __name__ == "__main__":
    app.run(port=8000,debug=True)