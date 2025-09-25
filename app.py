# app.py

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# --- Configuração Inicial ---
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'santo_antonio_super_mais_2024'
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# --- Modelos (Tabelas do Banco de Dados) ---
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com manutenções
    manutencoes = db.relationship('Manutencao', backref='loja', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Loja {self.nome}>'

class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    placa = db.Column(db.String(10), nullable=False, unique=True)
    modelo = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50))
    ano = db.Column(db.Integer)
    cor = db.Column(db.String(30))
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com manutenções
    manutencoes = db.relationship('Manutencao', backref='veiculo', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Veiculo {self.placa}>'

class Manutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)  # 'loja' ou 'veiculo'
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco_total = db.Column(db.Float, default=0.0)
    data_manutencao = db.Column(db.DateTime, default=datetime.utcnow)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chaves estrangeiras
    loja_id = db.Column(db.Integer, db.ForeignKey('loja.id'), nullable=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=True)
    
    # Relacionamento com fotos
    fotos = db.relationship('FotoManutencao', backref='manutencao', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Manutencao {self.titulo}>'

class FotoManutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(100), nullable=False)
    caminho_arquivo = db.Column(db.String(200), nullable=False)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chave estrangeira
    manutencao_id = db.Column(db.Integer, db.ForeignKey('manutencao.id'), nullable=False)
    
    def __repr__(self):
        return f'<FotoManutencao {self.nome_arquivo}>'


# --- Funções Auxiliares ---
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Rotas da Aplicação ---
@app.route('/')
def homepage():
    # Busca todas as lojas e todos os veículos no banco
    lista_de_lojas = Loja.query.all()
    lista_de_veiculos = Veiculo.query.all()
    
    # Busca manutenções recentes
    manutencoes_recentes = Manutencao.query.order_by(Manutencao.data_cadastro.desc()).limit(10).all()
    
    # Estatísticas
    total_lojas = len(lista_de_lojas)
    total_veiculos = len(lista_de_veiculos)
    total_manutencoes = Manutencao.query.count()
    
    # Envia todas as informações para o template
    return render_template('index.html', 
                         lojas=lista_de_lojas, 
                         veiculos=lista_de_veiculos,
                         manutencoes_recentes=manutencoes_recentes,
                         total_lojas=total_lojas,
                         total_veiculos=total_veiculos,
                         total_manutencoes=total_manutencoes)

# --- Rotas para Lojas ---
@app.route('/lojas')
def listar_lojas():
    lojas = Loja.query.all()
    return render_template('lojas.html', lojas=lojas)

@app.route('/lojas/cadastrar', methods=['GET', 'POST'])
def cadastrar_loja():
    if request.method == 'POST':
        nome_da_loja = request.form['nome_loja']
        endereco = request.form.get('endereco', '')
        telefone = request.form.get('telefone', '')
        
        nova_loja = Loja(nome=nome_da_loja, endereco=endereco, telefone=telefone)
        db.session.add(nova_loja)
        db.session.commit()
        flash('Loja cadastrada com sucesso!', 'success')
        return redirect(url_for('listar_lojas'))
        
    return render_template('cadastrar_loja.html')

@app.route('/lojas/<int:loja_id>')
def detalhes_loja(loja_id):
    loja = Loja.query.get_or_404(loja_id)
    manutencoes = Manutencao.query.filter_by(loja_id=loja_id).order_by(Manutencao.data_manutencao.desc()).all()
    return render_template('detalhes_loja.html', loja=loja, manutencoes=manutencoes)

# --- Rotas para Veículos ---
@app.route('/veiculos')
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return render_template('veiculos.html', veiculos=veiculos)

@app.route('/veiculos/cadastrar', methods=['GET', 'POST'])
def cadastrar_veiculo():
    if request.method == 'POST':
        placa_do_veiculo = request.form['placa_veiculo']
        modelo_do_veiculo = request.form['modelo_veiculo']
        marca = request.form.get('marca', '')
        ano = request.form.get('ano', type=int)
        cor = request.form.get('cor', '')
        
        novo_veiculo = Veiculo(placa=placa_do_veiculo, modelo=modelo_do_veiculo, 
                              marca=marca, ano=ano, cor=cor)
        db.session.add(novo_veiculo)
        db.session.commit()
        flash('Veículo cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_veiculos'))
        
    return render_template('cadastrar_veiculo.html')

@app.route('/veiculos/<int:veiculo_id>')
def detalhes_veiculo(veiculo_id):
    veiculo = Veiculo.query.get_or_404(veiculo_id)
    manutencoes = Manutencao.query.filter_by(veiculo_id=veiculo_id).order_by(Manutencao.data_manutencao.desc()).all()
    return render_template('detalhes_veiculo.html', veiculo=veiculo, manutencoes=manutencoes)

# --- Rotas para Manutenções ---
@app.route('/manutencoes')
def listar_manutencoes():
    tipo = request.args.get('tipo', 'todas')
    if tipo == 'loja':
        manutencoes = Manutencao.query.filter_by(tipo='loja').order_by(Manutencao.data_manutencao.desc()).all()
    elif tipo == 'veiculo':
        manutencoes = Manutencao.query.filter_by(tipo='veiculo').order_by(Manutencao.data_manutencao.desc()).all()
    else:
        manutencoes = Manutencao.query.order_by(Manutencao.data_manutencao.desc()).all()
    
    return render_template('manutencoes.html', manutencoes=manutencoes, tipo_atual=tipo)

@app.route('/manutencoes/cadastrar', methods=['GET', 'POST'])
def cadastrar_manutencao():
    if request.method == 'POST':
        tipo = request.form['tipo']
        titulo = request.form['titulo']
        descricao = request.form.get('descricao', '')
        preco_total = request.form.get('preco_total', 0, type=float)
        data_manutencao = request.form.get('data_manutencao')
        
        if data_manutencao:
            data_manutencao = datetime.strptime(data_manutencao, '%Y-%m-%d')
        else:
            data_manutencao = datetime.utcnow()
        
        nova_manutencao = Manutencao(
            tipo=tipo,
            titulo=titulo,
            descricao=descricao,
            preco_total=preco_total,
            data_manutencao=data_manutencao
        )
        
        if tipo == 'loja':
            loja_id = request.form.get('loja_id', type=int)
            if loja_id:
                nova_manutencao.loja_id = loja_id
        elif tipo == 'veiculo':
            veiculo_id = request.form.get('veiculo_id', type=int)
            if veiculo_id:
                nova_manutencao.veiculo_id = veiculo_id
        
        db.session.add(nova_manutencao)
        db.session.commit()
        
        # Upload de fotos
        if 'fotos' in request.files:
            fotos = request.files.getlist('fotos')
            fotos_uploaded = 0
            
            for foto in fotos:
                if foto and foto.filename and allowed_file(foto.filename):
                    try:
                        filename = secure_filename(foto.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                        filename = timestamp + filename
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        foto.save(filepath)
                        
                        foto_manutencao = FotoManutencao(
                            nome_arquivo=filename,
                            caminho_arquivo=filepath,
                            manutencao_id=nova_manutencao.id
                        )
                        db.session.add(foto_manutencao)
                        fotos_uploaded += 1
                        
                    except Exception as e:
                        print(f"Erro ao fazer upload da foto {foto.filename}: {str(e)}")
                        continue
            
            if fotos_uploaded > 0:
                flash(f'{fotos_uploaded} foto(s) anexada(s) com sucesso!', 'success')
        
        db.session.commit()
        flash('Manutenção cadastrada com sucesso!', 'success')
        return redirect(url_for('listar_manutencoes'))
    
    lojas = Loja.query.all()
    veiculos = Veiculo.query.all()
    return render_template('cadastrar_manutencao.html', lojas=lojas, veiculos=veiculos)

@app.route('/manutencoes/<int:manutencao_id>')
def detalhes_manutencao(manutencao_id):
    manutencao = Manutencao.query.get_or_404(manutencao_id)
    return render_template('detalhes_manutencao.html', manutencao=manutencao)

# --- Rota para servir arquivos de upload ---
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Rota para API de estatísticas ---
@app.route('/api/estatisticas')
def api_estatisticas():
    total_lojas = Loja.query.count()
    total_veiculos = Veiculo.query.count()
    total_manutencoes = Manutencao.query.count()
    total_gasto = db.session.query(db.func.sum(Manutencao.preco_total)).scalar() or 0
    
    return jsonify({
        'total_lojas': total_lojas,
        'total_veiculos': total_veiculos,
        'total_manutencoes': total_manutencoes,
        'total_gasto': float(total_gasto)
    })


# --- Inicialização do Banco de Dados ---
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Para produção (gunicorn)
    create_tables()