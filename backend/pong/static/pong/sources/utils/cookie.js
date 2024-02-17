export function SetCookie(name, value, path = "/")
{
    var expirationDate = new Date();
    expirationDate.setTime(expirationDate.getTime() + (1 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + expirationDate.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=" + path;
}

export function DeleteCookie(name)
{
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}