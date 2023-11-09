
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

function healthFormatter(value) {
    if (value) {
        if (value === "ok") {
            return `<div class="health-success"><i class="fas fa-check mr-1"></i>${value}</div>`;
        }

        return `<div class="health-danger"><i class="fas fa-ban mr-1"></i>${value}</div>`
    }

    return `<div class="health-warning"><i class="fas fa-question mr-1"></i>unknown</div>`
}

function deleteFormatter(value) {
    if (value) {
        return `<form method="post" action="/instances/${value}"><button type="submit" class="data-table link-danger" target="_blank"><i class="fas fa-trash mr-1"></i>Delete</button></form>`;
    }

    return ''
}
