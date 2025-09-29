# app.py

import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
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

# Inicialização das tabelas será feita após definição das classes

# Decorator para garantir que as tabelas existam em todas as rotas
def ensure_db_tables(func):
    """Decorator que garante que as tabelas existem antes de executar a função"""
    def wrapper(*args, **kwargs):
        try:
            with app.app_context():
                # Verificar se as tabelas existem fazendo uma query simples
                db.session.execute("SELECT 1 FROM loja LIMIT 1")
                # Garantir que temos usuários padrão
                if Usuario.query.count() == 0:
                    print("🔧 Tabelas OK, mas não há usuários. Criando agora...")
                    create_default_users_if_needed()
        except Exception:
            # Se não existem, criar agora
            try:
                with app.app_context():
                    db.create_all()
                    db.session.commit()
                    print("🔧 Tabelas criadas durante requisição")
                    # Criar usuários padrão também
                    create_default_users_if_needed()
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

# Modelo Usuario removido - sistema sem autenticação


# Função para criar usuários removida - sistema sem autenticação

# Função para garantir criação das tabelas após todas as classes estarem definidas
def ensure_tables_created():
    """Força criação das tabelas no startup"""
    try:
        with app.app_context():
            print("🔧 Garantindo criação das tabelas no startup...")
            db.create_all()
            db.session.commit()
            print("✅ Todas as tabelas criadas com sucesso!")
            
    except Exception as e:
        print(f"⚠️  Erro garantindo tabelas: {e}")
        db.session.rollback()
        try:
            with app.app_context():
                db.create_all()
                db.session.commit()
                print("✅ Tabelas criadas na segunda tentativa!")
        except Exception as e2:
            print(f"❌ Erro crítico criando tabelas: {e2}")

# Executar na inicialização do módulo sempre
# Se não há DATABASE_URL (desenvolvimento local), roda na primeira startup
if os.environ.get('DATABASE_URL'):
    # Produção - Render
    ensure_tables_created()
else:
    # Desenvolvimento local ou primeira vez
    try:
        print("🔧 Executando setup inicial (desenvolvimento local)...")
        ensure_tables_created()
    except Exception as e:
        print(f"⚠️ Erro no setup inicial (ok se é primeira vez): {e}")

# Decorators de autenticação removidos - sistema sem login


# --- Rotas da Aplicação ---
@app.route('/')
@ensure_db_tables
def homepage():
    # Redirecionar para a página de manutenções como página principal
    return redirect(url_for('listar_manutencoes'))

# --- Rotas para Lojas ---
@app.route('/lojas')
@ensure_db_tables
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
    
    # Debug: verificar fotos
    print(f"🔍 Debug - Manutenção {manutencao_id}:")
    print(f"   - Título: {manutencao.titulo}")
    print(f"   - Fotos encontradas: {len(manutencao.fotos) if manutencao.fotos else 0}")
    
    if manutencao.fotos:
        for i, foto in enumerate(manutencao.fotos):
            print(f"   - Foto {i+1}: {foto.nome_arquivo}")
            print(f"     Caminho: {foto.caminho_arquivo}")
            print(f"     Existe arquivo: {os.path.exists(foto.caminho_arquivo)}")
    
    return render_template('detalhes_manutencao.html', manutencao=manutencao)

@app.route('/manutencoes/<int:manutencao_id>/editar', methods=['GET', 'POST'])
def editar_manutencao(manutencao_id):
    manutencao = Manutencao.query.get_or_404(manutencao_id)
    
    if request.method == 'POST':
        # Atualizar dados da manutenção
        manutencao.titulo = request.form['titulo']
        manutencao.descricao = request.form.get('descricao', '')
        manutencao.preco_total = request.form.get('preco_total', 0, type=float)
        
        # Atualizar data se fornecida
        data_manutencao = request.form.get('data_manutencao')
        if data_manutencao:
            manutencao.data_manutencao = datetime.strptime(data_manutencao, '%Y-%m-%d')
        
        # Atualizar loja ou veículo
        if manutencao.tipo == 'loja':
            loja_id = request.form.get('loja_id', type=int)
            manutencao.loja_id = loja_id if loja_id else None
        elif manutencao.tipo == 'veiculo':
            veiculo_id = request.form.get('veiculo_id', type=int)
            manutencao.veiculo_id = veiculo_id if veiculo_id else None
        
        db.session.commit()
        flash('Manutenção atualizada com sucesso!', 'success')
        return redirect(url_for('detalhes_manutencao', manutencao_id=manutencao.id))
    
    # Buscar lojas e veículos para o formulário
    lojas = Loja.query.all()
    veiculos = Veiculo.query.all()
    
    return render_template('editar_manutencao.html', 
                         manutencao=manutencao, 
                         lojas=lojas, 
                         veiculos=veiculos)

@app.route('/manutencoes/<int:manutencao_id>/apagar', methods=['POST'])
def apagar_manutencao(manutencao_id):
    manutencao = Manutencao.query.get_or_404(manutencao_id)
    
    # Apagar fotos associadas
    for foto in manutencao.fotos:
        # Remover arquivo físico
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.nome_arquivo)
        if os.path.exists(foto_path):
            os.remove(foto_path)
        
        # Remover do banco
        db.session.delete(foto)
    
    # Apagar manutenção
    db.session.delete(manutencao)
    db.session.commit()
    
    flash('Manutenção apagada com sucesso!', 'success')
    return redirect(url_for('listar_manutencoes'))

# --- Rota de Análise/Analytics ---
@app.route('/analise')
@ensure_db_tables
def analise():
    # Parâmetros de filtro
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    tipo_manutencao = request.args.get('tipo', 'todas')  # 'todas', 'loja', 'veiculo'
    
    # Query base para manutenções
    query = Manutencao.query
    
    # Aplicar filtros
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
            query = query.filter(Manutencao.data_manutencao >= data_inicio_obj)
        except ValueError:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d')
            query = query.filter(Manutencao.data_manutencao <= data_fim_obj)
        except ValueError:
            pass
    
    if tipo_manutencao != 'todas':
        query = query.filter(Manutencao.tipo == tipo_manutencao)
    
    # Buscar manutenções filtradas
    manutencoes = query.order_by(Manutencao.data_manutencao.desc()).all()
    
    # Cálculos de análise
    total_manutencoes = len(manutencoes)
    total_gasto = sum(m.preco_total for m in manutencoes)
    
    # Análise por tipo
    manutencoes_loja = [m for m in manutencoes if m.tipo == 'loja']
    manutencoes_veiculo = [m for m in manutencoes if m.tipo == 'veiculo']
    
    gasto_loja = sum(m.preco_total for m in manutencoes_loja)
    gasto_veiculo = sum(m.preco_total for m in manutencoes_veiculo)
    
    # Análise por loja
    lojas_analise = {}
    for manutencao in manutencoes_loja:
        if manutencao.loja:
            loja_nome = manutencao.loja.nome
            if loja_nome not in lojas_analise:
                lojas_analise[loja_nome] = {'total': 0, 'gasto': 0}
            lojas_analise[loja_nome]['total'] += 1
            lojas_analise[loja_nome]['gasto'] += manutencao.preco_total
    
    # Análise por veículo
    veiculos_analise = {}
    for manutencao in manutencoes_veiculo:
        if manutencao.veiculo:
            veiculo_placa = manutencao.veiculo.placa
            if veiculo_placa not in veiculos_analise:
                veiculos_analise[veiculo_placa] = {'total': 0, 'gasto': 0}
            veiculos_analise[veiculo_placa]['total'] += 1
            veiculos_analise[veiculo_placa]['gasto'] += manutencao.preco_total
    
    # Análise mensal (últimos 12 meses)
    from collections import defaultdict
    manutencoes_mensais = defaultdict(lambda: {'total': 0, 'gasto': 0})
    
    for manutencao in manutencoes:
        mes_ano = manutencao.data_manutencao.strftime('%Y-%m')
        manutencoes_mensais[mes_ano]['total'] += 1
        manutencoes_mensais[mes_ano]['gasto'] += manutencao.preco_total
    
    # Ordenar por mês
    manutencoes_mensais_ordenadas = dict(sorted(manutencoes_mensais.items()))
    
    # Análise por prioridade removida - campo não existe no modelo
    
    # Dados para o template
    dados_analise = {
        'filtros': {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'tipo': tipo_manutencao
        },
        'resumo': {
            'total_manutencoes': total_manutencoes,
            'total_gasto': total_gasto,
            'gasto_loja': gasto_loja,
            'gasto_veiculo': gasto_veiculo,
            'manutencoes_loja': len(manutencoes_loja),
            'manutencoes_veiculo': len(manutencoes_veiculo)
        },
        'lojas_analise': lojas_analise,
        'veiculos_analise': veiculos_analise,
        'manutencoes_mensais': manutencoes_mensais_ordenadas,
        'manutencoes': manutencoes[:20]  # Últimas 20 para preview
    }
    
    return render_template('analise.html', **dados_analise)

# --- Rota para servir arquivos de upload ---
# --- ROTAS DE LOGIN E AUTENTICAÇÃO REMOVIDAS ---

# Rota setup-admin removida - sistema sem autenticação

# Rota cadastro de usuário removida - sistema sem autenticação


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        # Se o arquivo não for encontrado, retornar uma imagem placeholder
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'placeholder.jpg', mimetype='image/jpeg')

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