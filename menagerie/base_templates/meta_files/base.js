$(document).ready(() => {
    $(".menagerie-copy-button").click((e) => {
        const text = $(e.currentTarget).siblings("code").text();
        navigator.clipboard.writeText(text);
    });
});