$(document).ready(() => {
    $(".menagerie-copy-button").click((e) => {
        const text = $(e.target).parent().siblings("code").text();
        navigator.clipboard.writeText(text);
    });
});