# WordPress com Nginx e MySQL em Docker Compose

Este projeto utiliza **Docker Compose** para criar um ambiente com múltiplos contêineres, simulando uma arquitetura com **balanceamento de carga**.

A aplicação é composta por:

- **1 contêiner Nginx**
- **3 contêineres WordPress**
- **1 contêiner MySQL**

## Objetivo do projeto

O objetivo é disponibilizar uma estrutura em que o **Nginx** receba as requisições do usuário e distribua o tráfego entre três instâncias do **WordPress**, enquanto todas elas utilizam o mesmo banco de dados **MySQL** e a mesma pasta de arquivos compartilhada.

Dessa forma, independentemente de qual contêiner WordPress responda, o conteúdo exibido será o mesmo.

---

## O que o `docker-compose.yml` faz

O arquivo `docker-compose.yml` é responsável por definir e orquestrar todos os serviços do projeto.

### Serviços criados

#### MySQL
O serviço `mysql` executa o banco de dados da aplicação.  
Ele é utilizado pelos três contêineres do WordPress e **não fica acessível diretamente pela máquina hospedeira**, apenas pela rede interna do Docker.

#### WordPress
Os serviços `wordpress1`, `wordpress2` e `wordpress3` executam três instâncias da aplicação WordPress.  
Todos se conectam ao mesmo banco MySQL e compartilham a mesma pasta da máquina hospedeira em `/var/www/html`.

Esses contêineres **não possuem portas publicadas**, portanto **não podem ser acessados diretamente** pelo navegador da máquina hospedeira.

#### Nginx
O serviço `nginx` atua como ponto de entrada da aplicação.  
Ele é o único contêiner com porta exposta para a máquina hospedeira, permitindo o acesso pelo navegador através da porta 80.

Além disso, o Nginx também monta a mesma pasta compartilhada dos contêineres WordPress, mas no caminho `/usr/share/nginx/html`, conforme exigido no projeto.

---

## O que o `nginx.conf` faz

O arquivo `nginx.conf` define a configuração do Nginx.

### Funções principais

#### 1. Configuração do upstream
O bloco `upstream wordpress` cria um grupo com os três servidores WordPress:

- `wordpress1`
- `wordpress2`
- `wordpress3`

Esse grupo permite que o Nginx faça o **balanceamento de carga** entre eles.

#### 2. Escuta na porta 80
O Nginx é configurado para escutar na porta 80, recebendo as requisições vindas do navegador.

#### 3. Encaminhamento das requisições
Quando o usuário acessa a aplicação, o Nginx encaminha a requisição para um dos contêineres WordPress definidos no upstream.

#### 4. Cabeçalho de identificação
A configuração adiciona o cabeçalho:

`X-Upstream`

Esse cabeçalho informa qual servidor WordPress respondeu à requisição, sendo útil para testar e comprovar o balanceamento de carga.

---

## Comunicação entre os contêineres

Todos os contêineres estão conectados à mesma rede Docker, o que permite a comunicação interna entre eles.

Fluxo da aplicação:

1. O usuário acessa o Nginx
2. O Nginx recebe a requisição
3. O Nginx encaminha para um dos contêineres WordPress
4. O WordPress consulta ou grava dados no MySQL
5. A resposta retorna ao usuário

---

## Compartilhamento de arquivos

Os três contêineres WordPress compartilham a mesma pasta da máquina hospedeira em:

`/var/www/html`

O contêiner Nginx também utiliza essa mesma pasta, porém mapeada para:

`/usr/share/nginx/html`

Isso garante que os arquivos da aplicação permaneçam sincronizados entre os serviços.

---

## Segurança e isolamento

O projeto foi configurado para que:

- **apenas o Nginx** seja acessível pela máquina hospedeira
- os contêineres **WordPress não sejam acessados diretamente**
- o contêiner **MySQL também não seja acessado diretamente**

Isso atende aos requisitos da atividade e mantém a arquitetura mais organizada.

---

## Como executar

Na pasta do projeto, execute:

```bash
docker compose up -d