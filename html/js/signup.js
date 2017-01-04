name_pass_re = new RegExp("[a-zA-Z0-9]{6,16}");
email_re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

function matchRE(r, text) {
	match = r.exec(text);
	if (match == null) {
		return false;
	}
	if (match[0] != text) {
		return false;
	}
	return true;
}

function checkusername() {
	username = $("[name=s_username]")[0]
	username.style.borderColor = "#ccc"

	if (username.value == "") {
		username.style.borderColor = "red"
		return false;
	}
	match = matchRE(name_pass_re, username.value)
	if (!match) {
		username.style.borderColor = "red"
		return false;
	}
	return true
}
function checkemail() {
	email = $("[name=s_email]")[0]
	email.style.borderColor = "#ccc"

	if (email.value == "") {
		email.style.borderColor = "red"
		return false;
	}
	match = matchRE(email_re, email.value)
	if (!match) {
		email.style.borderColor = "red"
		return false;
	}
	return true;
}
function checkpassword() {
	password = $("[name=s_password]")[0]
	password.style.borderColor = "#ccc"

	if (password.value == "") {
		password.style.borderColor = "red"
		return false;
	}
	match = matchRE(name_pass_re, password.value)
	if (!match) {
		password.style.borderColor = "red"
		return false;
	}
	return true
}
function checkintro() {
	inro = $("[name=s_intro]")[0]
	inro.style.borderColor = "#ccc"

	if (inro.value == "") {
		inro.style.borderColor = "red"
		return false;
	}
	return true
}
function checkcontact() {
	contact = $("[name=s_contact]")[0]
	contact.style.borderColor = "#ccc"

	if (contact.value == "") {
		contact.style.borderColor = "red"
		return false;
	}
	return true
}
function checkname() {
	$("[name=s_name]")[0].style.borderColor = "#ccc"

	if ($("[name=s_name]")[0].value == "") {
		$("[name=s_name]")[0].style.borderColor = "red"
		return false;
	}
	return true
}

function signup() {
	u_pass = checkusername()
	e_pass = checkemail()
	p_pass = checkpassword()
	n_pass = checkname()
	i_pass = checkintro()
	c_pass = checkcontact()

	if (u_pass && e_pass && p_pass && n_pass && i_pass && c_pass) {
		$("#s_password")[0].type = "password";
		$("#signup")[0].submit()
	}
}

function showpwd() {
	pwd = $("#s_password")[0]
	if (pwd.type == "password") {
		pwd.type = "text";
	}
	else {
		pwd.type = "password";
	}
}

function login() {
	username = $("[name=l_username]")[0]
	password = $("[name=l_password]")[0]

	err = false;
	if (username.value == "") {
		username.style.borderColor = "red";
		err = true;
	}
	if (password.value == "") {
		password.style.borderColor = "red";
		err = true;
	}

	if (!err) {
		$("#login")[0].submit()
	}
}