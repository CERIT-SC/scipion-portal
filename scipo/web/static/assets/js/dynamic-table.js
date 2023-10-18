
$(document).ready(function () {
    $table = $("table.data-table");
    $table.bootstrapTable({
        pagination: true,
        sidePagination: "server",
        sortable: true,
        sortReset: true,
        filterControl: true
    })
});

function linkFormatter(value) {
    if (value) {
        return `<a href="${value}" target="_blank"><i class="fas fa-link mr-1"></i>Open</a>`;
    }

    return ''
}
