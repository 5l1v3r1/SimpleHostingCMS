%if not user_exist:
	<form action="/register" method="post">
	    Почтовый адрес: <input name="email" type="text" /><br>
	    Имя: <input name="name" type="text" /><br>
	    Пароль: <input name="password" type="password" /><br>
	    <input value="Зарегистрировать" type="submit" />
	</form>
%else: 
	Такой email уже зарегистрирован
%end
