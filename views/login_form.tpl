%if not logined:
	<form action="/login" method="post">
	    Логин: <input name="username" type="text" /><br>
	    Пароль: <input name="password" type="password" /><br>
	    <a href="/register">Регистрация &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>
	    <input value="Войти" type="submit" />
	</form>
%else: 
	<form action="/logout" method="post">
		Welcome {{user}} <input value="Выйти" type="submit">
	</form>	
%end
