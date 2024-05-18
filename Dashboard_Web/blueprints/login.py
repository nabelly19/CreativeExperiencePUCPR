from flask import Blueprint, request, render_template, redirect, url_for

login = Blueprint("login",__name__, template_folder="templates") #Esta linha cria um novo blueprint chamado ‘login’. O segundo argumento, __name__, é o nome do módulo onde o blueprint é definido (neste caso, é o módulo atual). O argumento template_folder especifica o diretório onde o Flask deve procurar por templates para este blueprint.

users = {
    "user1":"1234",
    "user2":"12345",
    "user3":"12345",
    "user4":"12345",
    "user5":"12345",
    "user6":"12345",
    "user7":"12345",
    "user8":"12345"
}

adm = {
    "adm1":"1234",
    "adm2":"1234",
    "adm3":"1234",
    "adm4":"1234",
    "adm5":"1234",
    "adm6":"1234",
    "adm7":"1234",
    "adm8":"1234"
}

@login.route('/login_user')
def login_user():
    return render_template('homeLogin.html')


@login.route('/validated_user', methods=['POST'])
def validated_user():   
    invalid_credentials = False
    user = request.form.get('user')
    password = request.form.get('password')

    if request.method == 'POST':
        if user in users and users[user] == password:
            return redirect('/dashboard')
        elif user in adm and adm[user] == password:
            return redirect('/dashboard_adm')
        else:
            invalid_credentials = True

    return render_template('homeLogin.html', invalid_credentials=invalid_credentials, user=user)


@login.route('/register_user')
def register_user():
    return render_template("registerUser.html") # Encaminha o usuário para um formulário


@login.route('/add_user', methods=['GET','POST'])
def add_user():
    global users, adm # faz uso do dicionário global criado no início do código
    if request.method == 'POST': # Verifica se o método de comunicação que usuário solicitou é POST
        user = request.form['user'] # Caso seja, define uma variável "user" que recebe o que o usuário inseriu no input de name 'user'
        password = request.form['password'] # Além de criar uma variável "password" que recebe o preenchimento do input de name 'password'
        confirm_password = request.form['confirm_password'] # Futuramente fazer verificação
        user_type = request.form['user_type']
        if user_type == 'user': # Se o usuário a ser cadastrado seja um usuário comum
            users[user] = password # Salvar no dicionário users
        elif user_type == 'adm': # Se o usuário a ser cadastrado seja um adm
            adm[user] = password # Salvar no dicionário adm
    else:
        user = request.args.get('user', None) # Se a solicitação não for ‘POST’ (ou seja, é ‘GET’), estas linhas tentam obter os valores dos parâmetros ‘user’ e ‘password’ da string de consulta da solicitação. Se esses parâmetros não estiverem presentes, eles serão definidos como None.
        password = request.args.get('password', None)
        confirm_password = request.args.get('confirm_password', None)
        users[user] = password # Esta linha adiciona o usuário e a senha ao dicionário "users"
    return redirect("/list_users")
    
@login.route('/list_users')
def list_users():
    global users, adm
    return render_template("userList.html", users=users, adm=adm)

@login.route('/remove_user')
def remove_user():
    return render_template("listar_editar_remover", users=users)
                       
@login.route('/del_user', methods=['GET','POST'])
def del_user():
    global users
    if request.method == 'POST':
        user = request.form['user']
    else:
        user = request.args.get('user', None)
    users.pop(user)
    return render_template("listar_editar_remover", users=users)
