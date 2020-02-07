//создать XML объект для AJAX
function AjaxObj()
{
	var xml;
		try
		{
			xml = new XMLHttpRequest();
		}
		catch(e)
		{
			xml = false;
		}
	
	if (!xml)
		alert("Error");
	else
		return xml;
}