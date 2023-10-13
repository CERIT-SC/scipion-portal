
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
