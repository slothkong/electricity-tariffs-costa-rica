window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside = window.dash_clientside.clientside || {};

window.dash_clientside.clientside.toggle_theme = function(switchOn) {
    document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');
    return window.dash_clientside.no_update;
};