
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

function statusFormatter(value) {
    let iconClass, statusText, healthClass;

    statusText = value;

    switch (value) {
        case "stage-in":
            iconClass = "fas fa-download";
            healthClass = "health-success";
            break;
        case "running":
            iconClass = "fas fa-check";
            healthClass = "health-success";
            break;
        case "stage-out":
            iconClass = "fas fa-upload";
            healthClass = "health-success";
            break;
        case "finished":
            iconClass = "fas fa-door-open";
            healthClass = "health-success";
            break;
        case "failed_mount":
        case "project_locked":
        case "lock_error":
        case "sync_error":
        case "degraded":
            iconClass = "fas fa-ban";
            healthClass = "health-danger";
            break;
        default:
            iconClass = "fas fa-question";
            healthClass = "health-warning";
            statusText = "unknown";
    }

    return `<div class="${healthClass}"><i class="${iconClass} mr-1"></i>${statusText}</div>`;
}


function deleteFormatter(value) {
    if (value) {
        return `<form method="post" action="/instances_delete/${value}"><button type="submit" class="data-table link-danger" target="_blank"><i class="fas fa-trash mr-1"></i>Delete</button></form>`
    }

    return ''
}
