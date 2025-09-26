# app.py

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuração simples direta
USE_ADVANCED_CONFIG = False

# --- Configuração Inicial ---
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # PostgreSQL (Render Production)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    print("🌐 Conectando ao PostgreSQL (Render)...")
else:
    # SQLite (Desenvolvimento Local)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    print("💾 Usando SQLite (Modo Desenvolvimento)...")

# Configurações gerais
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'santo_antonio_super_mais_2024')
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar banco de dados
db = SQLAlchemy(app)

# Garantir que as tabelas sejam criadas na inicialização
def ensure_tables_created():
    """Força criação das tabelas no startup"""
    try:
        with app.app_context():
            print("🔧 Garantindo criação das tabelas no startup...")
            db.create_all()
            db.session.commit()  # Garantir que a transação seja commitada
            print("✅ Todas as tabelas criadas com sucesso!")
            
            # Criar usuários padrão
            create_default_users()
            
    except Exception as e:
        print(f"⚠️  Erro garantindo tabelas: {e}")
        db.session.rollback()
        
        # Tentar novamente
        try:
            with app.app_context():
                db.create_all()
                db.session.commit()
                print("✅ Tabelas criadas na segunda tentativa!")
                create_default_users()
        except Exception as e2:
            print(f"❌ Erro crítico criando tabelas: {e2}")

def create_default_users():
    """Cria usuários padrão se não existirem"""
    try:
        # Verificar se já existem usuários
        existing_users = Usuario.query.count()
        print(f"👥 Verificando usuários existentes: {existing_users}")
        
        if existing_users > 0:
            users_list = Usuario.query.all()
            print("📋 Usuários no sistema:")
            for u in users_list:
                print(f"   - {u.username} ({u.tipo}) - Ativo: {u.ativo}")
            return
        
        print("🆕 Criando usuários padrão...")
        
        # Criar usuário administrador
        admin_user = Usuario(
            username='admin',
            password='admin123',
            tipo='analista'
        )
        
        # Criar usuário comum de teste
        test_user = Usuario(
            username='usuario',
            password='123456',
            tipo='usuario'
        )
        
        db.session.add(admin_user)
        db.session.add(test_user)
        db.session.commit()
        
        # Confirmar que foram criados
        final_count = Usuario.query.count()
        print(f"✅ Usuários padrão criados! Total: {final_count}")
        print("   📧 Admin: admin / admin123")
        print("   📧 Usuário: usuario / 123456")
        
        # Verificar na mão para garantir que funciona
        test_admin = Usuario.query.filter_by(username='admin').first()
        if test_admin:
            print(f"🔐 Teste admin: IDF={test_admin.id}, Ativo={test_admin.ativo}, Senha={test_admin.verificar_senha('admin123')}")
        
    except Exception as e:
        print(f"⚠️  Erro criando usuários padrão: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()

# Executar na inicialização do módulo quando DATABASE_URL está presente
if os.environ.get('DATABASE_URL'):
    ensure_tables_created()

# Decorator para garantir que as tabelas existam em todas as rotas
def ensure_db_tables(func):
    """Decorator que garante que as tabelas existem antes de executar a função"""
    def wrapper(*args, **kwargs):
        try:
            with app.app_context():
                # Verificar se as tabelas existem fazendo uma query simples
                db.session.execute("SELECT 1 FROM loja LIMIT 1")
        except Exception:
            # Se não existem, criar agora
            try:
                with app.app_context():
                    db.create_all()
                    db.session.commit()
                    print("🔧 Tabelas criadas durante requisição")
            except Exception as e:
                print(f"⚠️  Erro criando tabelas durante request: {e}")
        
        return func(*args, **kwargs)
    
    # Manter o nome da função original para Flask routing
    wrapper.__name__ = func.__name__
    return wrapper

# --- Funções Auxiliares ---
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_routes(app):
    """Registrar todas as rotas na aplicação"""
    # Todas as rotas serão registradas aqui
    pass

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

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default='usuario')  # 'usuario' ou 'analista'
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'
    
    def verificar_senha(self, password):
        # Para simplicidade, vamos usar senhas em texto
        # Em produção seria melhor usar hash
        return self.password == password
    
    @property
    def is_analista(self):
        return self.tipo == 'analista'


# Decorator para verificar login
def login_required(func):
    """Decorator que verifica se o usuário está logado"""
    def wrapper(*args, **kwargs):
        session_user_id = session.get('user_id')
        session_username = session.get('username')
        print(f"🔒 Decorator login_required - User ID: {session_user_id}, Username: {session_username}")
        
        if not session_user_id:
            print("❌ Não logado: redirecionando para login")
            flash('Você precisa fazer login para acessar essa página.', 'warning')
            return redirect(url_for('login'))
        
        print(f"✅ Usuário logado - ID: {session_user_id}")
        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper

# Decorator para verificar se é analista
def analista_required(func):
    """Decorator que verifica se o usuário é analista"""
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Você precisa fazer login para acessar essa página.', 'warning')
            return redirect(url_for('login'))
        
        user = Usuario.query.get(session['user_id'])
        if not user or not user.is_analista:
            flash('Apenas analistas podem acessar essa área.', 'error')
            return redirect(url_for('homepage'))
        
        return func(*args, **kwargs)
    
    wrapper.__name__ = func.__name__
    return wrapper


# --- Rotas da Aplicação ---
@app.route('/')
@ensure_db_tables
@login_required
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
@ensure_db_tables
@login_required
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
@ensure_db_tables
@login_required
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
@ensure_db_tables
@login_required
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
# --- ROTAS DE LOGIN E AUTENTICAÇÃO ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        print(f"🔐 Tentativa de login: {username} / {password}")
        
        # Buscar usuário
        user = Usuario.query.filter_by(username=username, ativo=True).first()
        
        print(f"🔍 Usuário encontrado: {user}")
        if user:
            print(f"🔑 Verificando senha: {user.verificar_senha(password)}")
        
        if user and user.verificar_senha(password):
            # Login bem sucedido
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.tipo
            
            print(f"✅ Login bem-sucedido: {user.username} (ID: {user.id})")
            
            # Atualizar último login
            user.ultimo_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Bem-vindo, {user.username}!', 'success')
            print("🔄 Redirecionando para homepage...")
            
            # Testar redirecionamento passo a passo
            try:
                return redirect(url_for('homepage'))
            except Exception as redirect_error:
                print(f"❌ Erro no redirecionamento: {redirect_error}")
                return redirect('/')  # Fallback: redirect direto
        else:
            print(f"❌ Login falhou para: {username}")
            flash('Usuário ou senha incorretos.', 'error')
    
    # Se não está logado, mostrar tela de login
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('login'))

@app.route('/usuario/cadastro', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        tipo = request.form.get('tipo', 'usuario')
        
        # Verificar se usuário já existe
        if Usuario.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'error')
            return render_template('cadastrar_usuario.html')
        
        # Criar novo usuário
        novo_usuario = Usuario(
            username=username,
            password=password,
            tipo=tipo
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('homepage'))
    
    return render_template('cadastrar_usuario.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- Rota para API de estatísticas ---
@app.route('/api/estatisticas')
@ensure_db_tables
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

def init_database_tables():
    """Inicializa as tabelas do banco apenas se necessário"""
    with app.app_context():
        print("🔧 Verificando estrutura do banco...")
        
        if DATABASE_URL:
            print("📊 PostgreSQL detectado - criando tabelas...")
            try:
                db.create_all()
                print("✅ Schema PostgreSQL configurado!")
                return True
            except Exception as e:
                print(f"⚠️  Erro ao criar tabelas PostgreSQL: {e}")
                # Tentar novamente
                db.session.rollback()
                db.create_all()
                print("✅ Schema PostgreSQL configurado na segunda tentativa!")
                return True
        else:
            print("💾 SQLite detectado - criando/verificando tabelas...")
            try:
                db.create_all()
                print("✅ Schema SQLite configurado!")
                return True
            except Exception as e:
                print(f"❌ Erro crítico SQLite: {e}")
                return False

if __name__ == '__main__':
    print("🚀 Sistema de Manutenção - Supermercado")
    print("🔧 Configurando banco de dados...")
    
    # Detectar ambiente
    if DATABASE_URL:
        print("🌐 Ambiente: PRODUÇÃO (Render + PostgreSQL)")
    else:
        print("💾 Ambiente: DESENVOLVIMENTO (SQLite Local)")
    
    # Inicializar banco de dados
    init_database_tables()
    
    # Configurar porta
    port = int(os.environ.get('PORT', 5000))
    
    print(f"✅ Sistema iniciado na porta {port}")
    
    # Diferentes URLs dependendo do ambiente
    if os.environ.get('RENDER'):
        app_url = "https://sistema-manutencao-supermais.onrender.com"
        print(f"🌐 Render URL: {app_url}")
    else:
        app_url = f"http://localhost:{port}"
        print(f"🌐 Local URL: {app_url}")
    
    print(f"🔗 Acesse: {app_url}")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=not DATABASE_URL)