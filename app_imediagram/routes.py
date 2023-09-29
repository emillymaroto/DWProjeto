from flask import  render_template, url_for, redirect
from app_imediagram import app, bcrypt, database
from app_imediagram.forms import FormLogin, FormCriarConta, FormFoto
from flask_login import login_required, login_user, logout_user, current_user
from app_imediagram.models import Usuario, Foto
import os


@app.route('/', methods = [ "GET", "POST" ] )
def homepage():
    formlogin = FormLogin()

    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by( email = formlogin.email.data ).first()
        if usuario and bcrypt.check_password_hash( usuario.senha, formlogin.senha.data ):
            login_user( usuario )
            return redirect( url_for( "perfil" ), id_usuario = usuario.id )

    return render_template( 'homepage.html', form = formlogin )

@app.route('/criar-conta', methods = [ "GET", "POST" ] )
def criarconta():
    formcriarconta = FormCriarConta()

    if formcriarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash( formcriarconta.senha.data )
        usuario = Usuario( username = formcriarconta.username.data, senha = senha, email = formcriarconta.email.data )
        database.session.add( usuario )
        database.session.commit()

        login_user( usuario, remember = True )

        return redirect( url_for( "perfil", id_usuario = usuario.id ) )

    return render_template( 'criarconta.html', form = formcriarconta )

@app.route( '/logout' )
@login_required
def logout():
    logout_user()
    return redirect( url_for( "homepage" ) )

@app.route( '/feed' )
@login_required
def feed():
    fotos = Foto.query.order_by( Foto.data_criacao.desc() ).agotll()
    return render_template( "feed.html", fotos = fotos )

@app.route('/perfil/<id_usuario>', methods = [ "GET", "POST" ])
@login_required
def perfil( id_usuario ):

    if int( id_usuario ) == int( current_user.id ):
        formfoto = FormFoto()

        if formfoto.validate_on_submit():
            arquivo = formfoto.foto.data
            caminho = os.path.join( os.path.abspath( os.path.dirname( __file__ ) ), app.config['UPLOAD_FOLDER'], arquivo )

            arquivo.save( caminho )

            foto = Foto( imagem = arquivo, id_usuario = current_user.id )
            database.session.add( foto )
            database.session.commit()

        return render_template( "perfil.html", usuario = current_user, form = formfoto )
    else:
        usuario = Usuario.query.get( int( id_usuario ) )
        return render_template( 'perfil.html', usuario = usuario, form = None )