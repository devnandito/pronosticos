$(document).on("ready", inicio);
function inicio()
{
	$("input[type=checkbox]").on("click", marcar);
	$("input[type=checkbox]").attr("disabled", "disabled");
	$("label[for='user'] input[type=text]").attr("placeholder", "Usuario");
	$("label[for='pass'] input[type=password]").attr("placeholder", "Contraseña");
	$("label[for='pwd1'] input[type=password]").attr("placeholder", "Contraseña");
	$("label[for='pwd2'] input[type=password]").attr("placeholder", "Repita la Contraseña");
	$("#mail").attr("placeholder", "Correo electronico");
	$("label[for='usr'] input[type=text]").attr("placeholder", "Usuario");
	$("label[for='error']").addClass("error");
	$("#search").change(searchs);
}
function marcar()
{
	if ($(this).is(":checked"))
	{
		var group = "input:checkbox[name='"+$(this).attr("name")+"']";
		$(group).prop("checked", false);
		$(this).prop("checked", true);
	}
	else
	{
		$(this).prop("checked", false);
	}
}
function searchs()
{
	$.ajax({
		type: "GET",
		url: "/search",
		data: 
			{
				search_text: $("#search").val()/*,
				csrfmiddlewaretoken : $("input[name=csrfmiddlewaretoken]").val()*/
			},
		success: resultado,
		dataType: "html"
	});
}
function mostrar(url)
{
	$.ajax({
		url: url,
		type: "GET",
		success: resultado
	});
}
function resultado(data)
{
	$("#resultado").html(data);
}
/*function insert(url, id)
{
	var v1 = $(id).serialize();
	$.ajax({
		url: url,
		type: "POST",
		data: v1,
		success: resultado
	});
}*/
//var v1=$(id).serialize();
/*function marcar()
{
	if ($(this).is(":checked"))
	{
		var group = "input:checkbox[name='"+$(this).attr("name")+"']";
		$(group).prop("checked", false);
		$(this).prop("checked", true);
	}
	else
	{
		$(this).prop("checked", false);
	} 
}*/

