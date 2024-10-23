from flask import Flask, request,render_template,redirect,url_for,session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'contactos' in session and len(session['contactos']) > 0:
        return max(item['id'] for item in session['contactos']) + 1
    else:
        return 1

@app.route("/")
def index():
    if 'contactos' not in session:
        session['contactos'] = []
        
    contactos = session.get('contactos',[])
    return render_template('index.html',contactos=contactos)



@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        f_venc = request.form['f_venc']
        categoria = request.form['categoria']
        
        nuevo_contacto = {
            'id': generar_id(),
            'nombre':nombre,
            'cantidad':cantidad,
            'precio':precio,
            'f_venc':f_venc,
            'categoria':categoria,        
        }
        
        if 'contactos' not in session:
            session['contactos'] = []
            
        session['contactos'].append(nuevo_contacto)
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_contactos = session.get('contactos',[])
    contacto = next( (c for c in lista_contactos if c['id'] == id), None)
    if not contacto:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        
        contacto['nombre'] = request.form['nombre']
        contacto['cantidad'] = request.form['cantidad']
        contacto['precio'] = request.form['precio']
        contacto['f_venc'] = request.form['f_venc']
        contacto['categoria'] = request.form['categoria']
        
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html',contacto=contacto)
    
@app.route("/eliminar/<int:id>",methods=["POST"])
def eliminar(id):
    lista_contactos = session.get('contactos',[])
    contacto = next((c for c in lista_contactos if c['id'] == id),None)
    if contacto:
        session['contactos'].remove(contacto)
        session.modified = True
    return redirect(url_for('index'))
        

if __name__ == "__main__":
    app.run(debug=True)