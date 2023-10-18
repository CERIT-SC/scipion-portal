
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

function deleteFormatter(value) {
    if (value) {
        return `<a class="link-danger" href="/api/instance/delete/${value}" target="_blank"><i class="fas fa-trash mr-1"></i>Delete</a>`;
    }

    return ''
}
