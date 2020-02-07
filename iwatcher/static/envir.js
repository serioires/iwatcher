//Cookies
function getCookie(name){
  var matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {

  let date = new Date(Date.now() + 1728000e3);
  date = date.toUTCString();
  options = {
    path: '/',
    secure: true,
    date: date,
    // при необходимости добавьте другие значения по умолчанию
    ...options
  };

//  if (options.expires.toUTCString) {
//    options.expires = options.expires.toUTCString();
//  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }

  document.cookie = updatedCookie;
}

function deleteCookie(name) {
  setCookie(name, "", {
    'max-age': -1
  })
}
