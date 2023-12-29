$(document).ready(function() {
    console.log("Script loaded");

    const hiddenDiv = document.querySelector("#progress-bar");
    const downloadButtons = document.querySelectorAll(".download-btn");

    downloadButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            console.log("clicked");
            hiddenDiv.style.display = "block";
        });
    });
});

function pollProgress(playlistId) {
    $.ajax({
        url: '/long-polling-progress/' + playlistId,
        success: function(data) {
            if (data.progress !== 'timeout') {
                $('.progress-bar').css('width', data.progress + '%').attr('aria-valuenow', data.progress);
                if (parseInt(data.progress) === 100) {
                    clearInterval(intervalId);  // Zatrzymanie interwału
                    $('#progress-bar').hide();  // Ukrycie diva
                }
            }
        },
        error: function() {
            console.error('Błąd podczas pobierania postępu');
        }
    });
}

let intervalId = null;
function startPolling(playlistId) {
    const hiddenDiv = document.querySelector("#progress-bar");
    intervalId = setInterval( pollProgress, 1000, playlistId);
    if($('.progress-bar').attr('aria-valuenow') === '100') {
        clearInterval(intervalId);
        hiddenDiv.style.display = "none";
    }
}
