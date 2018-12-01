# Como iniciar o serviço

## Inicializando as instâncias

### Criando usuário e obtendo o key pair na AWS

Siga os passos para inicializar a(s) instância(s) inicial(is):

-Realizar login na AWS, acessar o dashboard "IAM", em seguida, "Users"

-Crie um usuário se não tiver um, em seguida acesse "Security Credentials" e crie um "Access Key" para o usuário

-Anote/baixe as credenciais (access key e secret access key)


### Clonando e criando as instâncias

-Clone o meu repositório utiliando:

git clone https://github.com/chends888/final_proj_cloud.git

-No diretório /final_proj_cloud você encontrará o arquivo setup_requirements.sh, execute-o:

./setup_requirements.sh


## Inicializando o load balancer:
-Realize login na AWS e crie a instância (com Ubuntu 18), esta máquina será seu load balancer

-Acesse a máquina


git clone

cd final_proj_cloud/

./requirements.sh

-aws configure, insira o seu access key e secret access key e como região insira us-east-1

-python3 loadbalancer.py


