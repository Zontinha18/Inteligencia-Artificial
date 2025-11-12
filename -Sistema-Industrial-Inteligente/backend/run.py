import time
from app import create_app
from models import db

def wait_for_db(app, max_retries=30):
    """Aguarda o banco de dados estar pronto"""
    print("🔄 Aguardando banco de dados MySQL...")
    for i in range(max_retries):
        try:
            with app.app_context():
                db.engine.connect()
            print("✅ Banco de dados conectado!")
            return True
        except Exception as e:
            print(f"⏳ Tentativa {i+1}/{max_retries}: {str(e)[:50]}")
            time.sleep(2)
    return False

if __name__ == '__main__':
    app = create_app('development')
    
    # Aguardar banco de dados
    if wait_for_db(app):
        # Criar tabelas
        with app.app_context():
            print("🔨 Criando tabelas no banco de dados...")
            db.create_all()
            print("✅ Tabelas criadas!")
        
        # Iniciar aplicação
        print("🚀 Iniciando servidor Flask na porta 5000...")
        print("📡 API disponível em: http://localhost:5000")
        print("📊 Adminer disponível em: http://localhost:8080")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Falha ao conectar ao banco de dados")