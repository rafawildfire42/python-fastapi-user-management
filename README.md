<h1 align="center"> Projeto </h1>

<h2>Observações:</h2>

<h3>Postgres:</h3>
- Caso use Windows, pode ser que tenha uma instância do Postgres rodando na porta 5432 e poderá ocorrer conflito com postgres rodando no container<br>
- Executar os seguintes comandos no terminal do Windows como administrador:<br>
> netstat -ano | findstr 5432<br>
> taskkill /f /pid _PID_<br>

<h3>Insomnia:</h3>
- No repositório tem um arquivo insomnia_paneas.yaml, onde é possível importar todos os endpoints e serem executados com o insomnia.<br>
- O token de acesso é atualizado automaticamente em todos os headers, mas o novo gerado pelo refresh token não, este deve ser inserido manualmente caso seja testado.<br>

<h3>Banco de dados:</h3>
- Para facilitar, o banco de dados já será populado com algumas informações.<br>
- Existem dois usuários cadastrados: **admin@mail.com** e **user@mail.com**<br>
- A senha de ambos os usuários é: **123456**<br>
- O usuário ADMIN pode acessar todos os endpoints e o USER apenas o metodo **GET** do endpoint /users<br>
- Para acessar o banco de dados por meio do Beekeeper, por exemplo, utilizar as seguintes credenciais:<br>
Host: localhost<br>
Port: 5432<br>
User: admin<br>
Password: paneas<br>
Default DB: main<br>

<h3>Envio de emails:</h3>
- O email é enviado assim que o usuário é criado através da API.<br>
- Para enviar emails é necessário resgatar uma chave, isso pode ser feito através do gmail.<br>
- Procedimentos: Acessar gmail > Clicar na foto de perfil > Gerenciar sua Conta do Google > Segurança > Verificação em duas etapas > Senhas de app (no final da página)<br>
- Após pegar essa chave de acesso, inserir no .env **(Isso deve ser realizado antes do BUILD!)**<br>

<h3>Documentação:</h3>
- A documentação da API pode ser acessada através do endereço http://localhost:8000/docs<br>
- A documentação é gerada com Swagger UI<br>

<h3>Principais documentações como referência:</h3>
- https://fastapi.tiangolo.com/tutorial/<br>
- https://alembic.sqlalchemy.org/en/latest/tutorial.html<br>
- https://docs.python.org/2/library/email-examples.html#id5<br>
- https://docs.docker.com/<br>
- https://docs.celeryq.dev/<br>

<h2>Inicializando o projeto:</h2>
<h3>Obs.: O projeto foi desenvolvido até o requisito 5.</h3>
- Clone o repositório: git clone git@github.com:rafawildfire42/fastapi-usermanagement.git<br>
- Pode ser necessário autenticação por ssh (https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)<br>
- Execute o comando: <br>
> docker build -t paneas .<br>
- Após finalizar o build, execute o seguinte comando:<br>
> docker compose up<br>
- Interagir com a aplicação por meio de ferramentas como Insomnia/Postman, Beekeeper (credenciais de acesso fornecidas acima), etc.
