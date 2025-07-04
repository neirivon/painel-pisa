from google.cloud import resource_manager
from google.oauth2 import service_account

# Caminho para o arquivo JSON da conta de serviço
SERVICE_ACCOUNT_JSON = '/home/neirivon/SINAPSE2.0/PISA/painel_pisa/utils/pisa-inclusao-streamlit-836b4678cd6e.json'

# Carregar credenciais da conta de serviço
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_JSON,
)

# Obter email da conta de serviço
sa_email = credentials.service_account_email

# Inicializar cliente do Resource Manager
client = resource_manager.Client(credentials=credentials)

# Listar projetos (opcional)
project_id = "pisa-inclusao-streamlit"  # substitua pelo ID do projeto onde quer verificar os papéis

# Obter políticas IAM do projeto
policy = client.projects().get_iam_policy(name=f"projects/{project_id}")

# Filtrar papéis atribuídos à conta de serviço
for binding in policy.bindings:
    if f"serviceAccount:{sa_email}" in binding.members:
        print(f"Papel encontrado: {binding.role}")
