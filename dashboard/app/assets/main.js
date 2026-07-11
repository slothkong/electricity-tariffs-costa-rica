window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside = window.dash_clientside.clientside || {};

window.dash_clientside.clientside.resize_chart = function(active_tab) {
    if (active_tab === 'chart-tab') {
        setTimeout(function() {
            const graphDiv = document.getElementById('chart');
            if (graphDiv && window.Plotly) {
                window.Plotly.Plots.resize(graphDiv);
            }
        }, 50);
    }
    return window.dash_clientside.no_update;
};

window.dash_clientside.clientside.toggle_theme = function(switchOn) {
    document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');
    return window.dash_clientside.no_update;
};
