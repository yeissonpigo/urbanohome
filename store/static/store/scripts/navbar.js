function active_navbar() {
    var navbar = document.getElementById('navbar')
    var navbar_session = document.getElementById('navbar_session')

    navbar.classList.toggle("active")
    navbar_session.classList.toggle("active")
    navbar.classList.toggle("slide")
    navbar_session.classList.toggle("slide")
}